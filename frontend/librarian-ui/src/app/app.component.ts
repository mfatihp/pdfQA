import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpEvent, HttpEventType } from '@angular/common/http';
import { PdfViewerModule } from 'ng2-pdf-viewer';
import { ViewChild, ElementRef, AfterViewChecked } from '@angular/core';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, PdfViewerModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})


export class AppComponent {
  @ViewChild('chatMessages') private chatMessagesRef!: ElementRef;
  constructor(private http: HttpClient) { }

  title = 'librarian-ui';
  userInput: string = '';
  messages: { sender: 'user' | 'bot'; text: string }[] = [];

  pdfSrc: string | Uint8Array | null = null;
  zoom: number = 1.0;

  uploadProgress = 0;
  isUploading: boolean = false;
  uploadComplete: boolean = false;
  selectedFile: File | null = null;

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  scrollToBottom() {
    try {
      this.chatMessagesRef.nativeElement.scrollTop = this.chatMessagesRef.nativeElement.scrollHeight;
    } catch (err) {
      console.error('Scroll failed:', err);
    }
  }

  sendMessage() {
    const messageText = this.userInput.trim();
    if (!messageText) return;

    this.messages.push({ sender: 'user', text: messageText });
    this.userInput = '';
    this.scrollToBottom();

    const text = messageText;

    this.http.post<{ reply: string }>('http://localhost:8000/answer', { text })
      .subscribe({
        next: (response) => {
          this.messages.push({ sender: 'bot', text: response.reply });
          setTimeout(() => this.scrollToBottom(), 100);
        },
        error: (err) => {
          this.messages.push({ sender: 'bot', text: 'Error: could not get a reply.' });
          console.error(err);
          setTimeout(() => this.scrollToBottom(), 100);
        }
      });
  }

  onFileSelected(event: any): void {
    this.uploadComplete = false;
    this.uploadProgress = 0;
    const file: File = event.target.files[0];

    if (file && file.type === 'application/pdf') {
      this.selectedFile = file;
      const reader = new FileReader();

      reader.onload = (e: any) => {
        this.pdfSrc = new Uint8Array(e.target.result);
      };

      reader.readAsArrayBuffer(file);
    } else {
      this.pdfSrc = null;
      alert('Please select a PDF file...');
    }
  }

  afterLoadComplete(): void {
    console.log('PDF loading is successful.')
  }

  onUploadClick(): void {
    if (!this.selectedFile) {
      alert('Select valid PDF file...');
      return;
    }

    const formData = new FormData();
    formData.append('pdf_file', this.selectedFile, this.selectedFile.name);

    this.isUploading = true;

    this.http.post('http://127.0.0.1:8000/upload', formData, {
      reportProgress: true,
      observe: 'events'
      }).subscribe({
        next: (event: HttpEvent<any>) => {
          if (event.type === HttpEventType.UploadProgress && event.total) {
            this.uploadProgress = Math.round((event.loaded / event.total) * 100);
          } else if (event.type === HttpEventType.Response) {
            this.isUploading = false;
            this.uploadComplete = true;
            setTimeout(() => this.uploadComplete = false, 2500); // reset thumbs up
          }
        },
        error: (err) => {
          console.error('Upload failed', err);
          this.isUploading = false;
          this.uploadComplete = false;
        }
      });
  }
}
