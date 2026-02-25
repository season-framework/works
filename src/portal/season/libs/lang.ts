import Service from './service';

export default class Lang {
    public value: string = "default";

    constructor(public service: Service) { }

    public async set(lang: string) {
        this.value = lang;
        await this.service.render();
    }

    public get() {
        return this.value;
    }
}