import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button],
  templateUrl: './settings.html',
  styleUrls: ['./settings.css']
})
export class Settings implements OnInit {
  activeTab: 'general' | 'security' | 'notifications' = 'general';
  successMessage = '';
  errorMessage = '';
  isSubmitting = false;

  language = 'English (US)';
  timezone = '(GMT+05:30) India Standard Time';
  dateFormat = 'DD/MM/YYYY';
  currency = 'INR (₹)';

  currentPassword = '';
  newPassword = '';
  confirmPassword = '';
  enableTwoFactor = false;
  sessionTimeout = '30 Minutes';

  emailNotifications = true;
  smsAlerts = false;
  deliveryDelayAlerts = true;
  contractExpiryAlerts = true;
  weeklySummaryEmail = true;

  theme: 'light' | 'dark' = 'light';
  compactSidebar = false;
  primaryColor = 'Indigo';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadSavedSettings();
  }

  loadSavedSettings(): void {
    const saved = localStorage.getItem('vrip_settings');
    if (saved) {
      try {
        const config = JSON.parse(saved);
        this.language = config.language || this.language;
        this.timezone = config.timezone || this.timezone;
        this.dateFormat = config.dateFormat || this.dateFormat;
        this.currency = config.currency || this.currency;
        this.enableTwoFactor = config.enableTwoFactor ?? this.enableTwoFactor;
        this.sessionTimeout = config.sessionTimeout || this.sessionTimeout;
        this.emailNotifications = config.emailNotifications ?? this.emailNotifications;
        this.smsAlerts = config.smsAlerts ?? this.smsAlerts;
        this.deliveryDelayAlerts = config.deliveryDelayAlerts ?? this.deliveryDelayAlerts;
        this.contractExpiryAlerts = config.contractExpiryAlerts ?? this.contractExpiryAlerts;
        this.theme = config.theme || 'light';
        this.compactSidebar = config.compactSidebar ?? false;

        this.applyTheme(this.theme);
      } catch (e) {
        console.error('Failed to parse settings', e);
      }
    }
  }

  selectTab(tab: 'general' | 'security' | 'notifications'): void {
    this.activeTab = tab;
    this.successMessage = '';
    this.errorMessage = '';
  }

  toggleTheme(selectedTheme: 'light' | 'dark'): void {
    this.theme = selectedTheme;
    this.applyTheme(selectedTheme);
  }

  applyTheme(t: 'light' | 'dark'): void {
    if (t === 'dark') {
      document.body.classList.add('dark-theme');
      document.body.style.backgroundColor = '#0f172a';
      document.body.style.color = '#f8fafc';
    } else {
      document.body.classList.remove('dark-theme');
      document.body.style.backgroundColor = '';
      document.body.style.color = '';
    }
  }

  saveGeneral(): void {
    this.saveSettingsToStorage();
    this.showSuccess('General preferences updated successfully.');
  }

  saveNotificationSettings(): void {
    this.saveSettingsToStorage();
    this.showSuccess('Notification preferences saved successfully.');
  }

  saveAppearanceSettings(): void {
    this.saveSettingsToStorage();
    this.showSuccess('Appearance and display theme updated successfully.');
  }

  changePassword(): void {
    this.errorMessage = '';
    this.successMessage = '';

    if (!this.currentPassword) {
      this.errorMessage = 'Please enter your current password.';
      return;
    }

    if (!this.newPassword || this.newPassword.length < 8) {
      this.errorMessage = 'New password must be at least 8 characters long.';
      return;
    }
    if (this.newPassword !== this.confirmPassword) {
      this.errorMessage = 'New password and confirm password do not match.';
      return;
    }

    this.isSubmitting = true;
    this.http.post('/auth/change-password', {
      current_password: this.currentPassword,
      new_password: this.newPassword
    }).subscribe({
      next: (res: any) => {
        this.isSubmitting = false;
        this.currentPassword = '';
        this.newPassword = '';
        this.confirmPassword = '';
        this.showSuccess(res.message || 'Password changed successfully!');
      },
      error: (err) => {
        this.isSubmitting = false;
        this.errorMessage = err.error?.detail || 'Failed to update password. Please check your current password.';
      }
    });
  }

  private saveSettingsToStorage(): void {
    const config = {
      language: this.language,
      timezone: this.timezone,
      dateFormat: this.dateFormat,
      currency: this.currency,
      enableTwoFactor: this.enableTwoFactor,
      sessionTimeout: this.sessionTimeout,
      emailNotifications: this.emailNotifications,
      smsAlerts: this.smsAlerts,
      deliveryDelayAlerts: this.deliveryDelayAlerts,
      contractExpiryAlerts: this.contractExpiryAlerts,
      theme: this.theme,
      compactSidebar: this.compactSidebar
    };
    localStorage.setItem('vrip_settings', JSON.stringify(config));
  }

  private showSuccess(msg: string): void {
    this.successMessage = msg;
    setTimeout(() => this.successMessage = '', 4000);
  }
}