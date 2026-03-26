import { Component } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule, RouterOutlet],
  templateUrl: './app.html',        // ✅ moved here
  styleUrls: ['./app.css']          // ✅ css linked here
})
export class AppComponent {}