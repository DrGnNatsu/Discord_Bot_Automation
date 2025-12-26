export interface Theme {
    isDarkMode: boolean;
    toggleTheme: (checked?: boolean) => void;
    initTheme: () => void;
}