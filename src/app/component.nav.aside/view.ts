import { OnInit } from '@angular/core';
import { HostListener } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Project } from '@wiz/libs/portal/works/project';

export class Component implements OnInit {
    constructor(
        public service: Service,
        public project: Project,
    ) { }

    public async ngOnInit() {
        await this.service.init();
    }

    @HostListener('document:click')
    public clickout() {
        this.service.navbar.toggle(true);
    }

    public async logout() {
        const res = await this.service.alert.show({
            title: "Logout",
            status: "error",
            message: "정말 로그아웃하시겠습니까?",
            action: "logout",
            actionBtn: "error",
            cancel: "cancel",
        });
        if (!res) return;
        location.href = "/auth/logout?returnTo=/authenticate";
    }
}