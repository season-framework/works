import { OnInit, Input } from '@angular/core';
import { Service } from "@wiz/libs/portal/season/service";

export class Component implements OnInit {
    @Input() search = false;

    public constructor(
        public service: Service,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.load();
    }

    public text = "";
    public list = [];
    public async load() {
        this.list = [];
        const { code, data } = await wiz.call("load");
        if (code !== 200) return await this.service.error("Failed to load SAML IdP Providers");
        this.list = data;
        await this.service.render();
    }

    public filter(item) {
        const targets = ["key", "display_name"];
        const t = this.text.toLowerCase();
        for (let target of targets) {
            let tmp = item[target];
            if (tmp === undefined) continue;
            tmp = tmp.toLowerCase();
            if (tmp.includes(t)) return true;
        }
        return false;
    }
}