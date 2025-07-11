import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpEvent, HttpEventType } from '@angular/common/http';
import { PdfViewerModule } from 'ng2-pdf-viewer';
import { ViewChild, ElementRef } from '@angular/core';


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
    
    if (!messageText) return; // Ignore empty input

    // Append user's message to chat history
    this.messages.push({ sender: 'user', text: messageText });
    this.userInput = '';
    this.scrollToBottom();

    const text = messageText;

    // Send the message to the FastAPI backend and handle the response
    this.http.post<{ reply: string }>('http://localhost:8000/answer', { text })
      .subscribe({
        next: (response) => {
          // Add the bot's reply to the chat history
          this.messages.push({ sender: 'bot', text: response.reply });
          setTimeout(() => this.scrollToBottom(), 100);
        },
        error: (err) => {
          // Add an error message to the chat if the backend request fails
          this.messages.push({ sender: 'bot', text: 'Error: could not get a reply.' });
          console.error(err);
          setTimeout(() => this.scrollToBottom(), 100);
        }
      });
  }

  onFileSelected(event: any): void {
    // Reset upload state
    this.uploadComplete = false;
    this.uploadProgress = 0;
    
    const file: File = event.target.files[0];

    // Validate file type
    if (file && file.type === 'application/pdf') {
      this.selectedFile = file;
      const reader = new FileReader();

      // Convert the PDF file to a Uint8Array
      reader.onload = (e: any) => {
        this.pdfSrc = new Uint8Array(e.target.result);
      };

      reader.readAsArrayBuffer(file);
    } else {
      // Clear PDF data variable (pdfSrc) if an invalid file is selected
      this.pdfSrc = null;
      alert('Please select a PDF file...');
    }
  }

  onUploadClick(): void {
    if (!this.selectedFile) {
      alert('Select valid PDF file...');
      return;
    }

    const formData = new FormData();
    formData.append('pdf_file', this.selectedFile, this.selectedFile.name);

    this.isUploading = true;
    
    // Send the PDF file to the FastAPI backend
    this.http.post('http://127.0.0.1:8000/upload', formData, {
      reportProgress: true,
      observe: 'events'
      }).subscribe({
        next: (event: HttpEvent<any>) => {
          if (event.type === HttpEventType.UploadProgress && event.total) {
            
            // Loading bar's progess calculation
            this.uploadProgress = Math.round((event.loaded / event.total) * 100);

          } else if (event.type === HttpEventType.Response) {
            this.isUploading = false;
            this.uploadComplete = true;
            setTimeout(() => this.uploadComplete = false, 2500);
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
