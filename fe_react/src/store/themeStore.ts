import type { Theme } from '@/types/theme';
import { create } from 'zustand';


export const useThemeStore = create<Theme>((set, get) => ({
    isDarkMode: false,
    toggleTheme: (checked) => {
        const newValue = checked !== undefined ? checked : !get().isDarkMode;
        set({ isDarkMode: newValue });
        if (typeof document !== 'undefined') {
            document.documentElement.classList.toggle('dark', newValue);
        }
    },
    initTheme: () => {
        const isDark = get().isDarkMode;
        if (typeof document !== 'undefined') {
            document.documentElement.classList.toggle('dark', isDark);
        }
    },
}));