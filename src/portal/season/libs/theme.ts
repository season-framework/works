import Service from './service';

export default class Theme {
    private _mode: 'light' | 'dark' = 'light';

    constructor(public service: Service) {
        this.load();
    }

    public get isDark(): boolean {
        return this._mode === 'dark';
    }

    public get current(): string {
        return this._mode;
    }

    public load() {
        try {
            const saved = localStorage.getItem('wiz-theme');
            if (saved === 'dark' || saved === 'light') {
                this._mode = saved;
            }
        } catch (e) { }
        this.apply();
    }

    public async toggle() {
        this._mode = this._mode === 'dark' ? 'light' : 'dark';
        try { localStorage.setItem('wiz-theme', this._mode); } catch (e) { }
        this.apply();
    }

    public async set(mode: 'light' | 'dark') {
        this._mode = mode;
        try { localStorage.setItem('wiz-theme', this._mode); } catch (e) { }
        this.apply();
    }

    private apply() {
        const html = document.documentElement;
        if (this._mode === 'dark') {
            html.classList.add('dark');
            html.setAttribute('data-theme', 'dark');
        } else {
            html.classList.remove('dark');
            html.setAttribute('data-theme', 'light');
        }
    }
}
