import { OnInit, OnDestroy } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { Subscription } from 'rxjs';
import { Service } from '@wiz/libs/portal/season/service';
import { Project } from '@wiz/libs/portal/works/project';

export class Component implements OnInit, OnDestroy {
    public PROJECT_ID: string = "";
    public MENU: string = "";

    public loaded: boolean = false;
    private routerSub: Subscription;

    constructor(public service: Service, public project: Project, private router: Router) {
        if (!WizRoute.segment.id)
            return service.href("/explore/project");
        this.PROJECT_ID = WizRoute.segment.id;
    }

    private isMenuAvailable(menu: string): boolean {
        if (menu === 'info' || menu === 'member') return true;
        const menuConfig = this.project.data()?.extra?.menu;
        if (!menuConfig) return false;
        return !!menuConfig[menu];
    }

    private getDefaultMenu(): string {
        return this.project.data()?.extra?.main || 'info';
    }

    public async ngOnInit() {
        await this.service.init();
        await this.service.auth.allow();
        await this.project.init(this.PROJECT_ID);

        if (!WizRoute.segment.menu) {
            let main: string = this.getDefaultMenu();
            this.service.href(`/project/${this.PROJECT_ID}/${main}`);
            this.MENU = main;
        } else {
            this.MENU = WizRoute.segment.menu;
        }

        if (!this.project.status())
            return this.service.href("/explore/project");
        
        await this.service.render();

        this.loaded = true;

        this.routerSub = this.router.events.subscribe(async (event) => {
            if (event instanceof NavigationEnd) {
                if (!this.loaded) return;
                const newId = WizRoute.segment.id;
                const newMenu = WizRoute.segment.menu;

                if (!newId) {
                    this.service.href("/explore/project");
                    return;
                }

                // 프로젝트 변경 감지: 프로젝트 re-init
                if (newId !== this.PROJECT_ID) {
                    this.PROJECT_ID = newId;
                    this.loaded = false;
                    await this.project.init(this.PROJECT_ID);

                    if (!this.project.status()) {
                        this.service.href("/explore/project");
                        return;
                    }

                    // 메뉴 결정: 요청된 메뉴가 사용 가능하면 유지, 아니면 메인 메뉴로
                    let targetMenu = newMenu;
                    if (!targetMenu || !this.isMenuAvailable(targetMenu)) {
                        targetMenu = this.getDefaultMenu();
                        this.MENU = targetMenu;
                        this.loaded = true;
                        this.service.href(`/project/${this.PROJECT_ID}/${targetMenu}`);
                        return;
                    }

                    this.MENU = targetMenu;
                    this.loaded = true;
                    await this.service.render();
                    return;
                }

                // 같은 프로젝트, 메뉴 변경
                if (!newMenu) {
                    this.service.href("/explore/project");
                    return;
                }
                if (newMenu !== this.MENU) {
                    this.MENU = newMenu;
                    await this.service.render();
                }
            }
        });

        await this.service.render();
    }

    public async ngOnDestroy() {
        if (this.routerSub) this.routerSub.unsubscribe();
        await this.project.revert();
        await this.service.render();
    }
}
