import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  constructor(private http: HttpClient) {}

  title = 'librarian-ui';
  userInput: string = '';
  messages: { sender: 'user' | 'bot'; text: string }[] = [];

  sendMessage() {
    const messageText = this.userInput.trim();
    if (!messageText) return;

    this.messages.push({ sender: 'user', text: messageText });
    this.userInput = '';

    const text = messageText;

    this.http.post<{ reply: string }>('http://localhost:8000/answer', { text })
    .subscribe({
      next: (response) => {
        this.messages.push({ sender: 'bot', text: response.reply });
      },
      error: (err) => {
        this.messages.push({ sender: 'bot', text: 'Error: could not get a reply.' });
        console.error(err);
      }
    });
  }
}
