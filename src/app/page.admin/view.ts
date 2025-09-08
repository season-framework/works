import { OnInit } from "@angular/core";
import { Service } from "src/libs/portal/season/service";

export class Component implements OnInit {

    constructor(
        public service: Service,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.service.auth.allow.membership("admin", "/explore/project");
    }
}