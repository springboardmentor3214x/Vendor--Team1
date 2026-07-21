import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private readonly THEME_KEY = 'vrip-theme-preference';
  public isDarkMode = false;

  constructor() {
    this.initTheme();
  }

  private initTheme() {
    // 1. Check localStorage
    const savedTheme = localStorage.getItem(this.THEME_KEY);
    if (savedTheme) {
      this.isDarkMode = savedTheme === 'dark';
    } else {
      // 2. Check OS preference
      this.isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    this.applyTheme();
  }

  public toggleTheme() {
    this.isDarkMode = !this.isDarkMode;
    localStorage.setItem(this.THEME_KEY, this.isDarkMode ? 'dark' : 'light');
    this.applyTheme();
  }

  private applyTheme() {
    if (this.isDarkMode) {
      document.body.setAttribute('data-theme', 'dark');
    } else {
      document.body.removeAttribute('data-theme');
    }
  }
}
