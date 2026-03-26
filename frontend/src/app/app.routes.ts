import { Routes } from '@angular/router';
import { ChatComponent } from './modules/chat/chat.component';

import { DashboardComponent } from './modules/dashboard/dashboard.component';

export const routes = [
  { path: '', component: ChatComponent },
  { path: 'dashboard', component: DashboardComponent }
];