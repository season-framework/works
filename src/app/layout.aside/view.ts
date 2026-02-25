import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    public isAside: boolean = false;

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        this.service.trigger.bind("isAside", this.isAside);
        await this.service.init();
    }

    public async hideAside() {
        this.isAside = !this.isAside;
        this.service.trigger.bind("isAside", this.isAside);
        await this.service.render();
    }
}