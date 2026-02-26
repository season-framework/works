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

    public async ngOnInit() {
        await this.service.init();
        await this.service.auth.allow();
        await this.project.init(this.PROJECT_ID);

        if (!WizRoute.segment.menu) {
            let main: string = this.project.data().extra.main;
            if (!main) main = 'info';
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
                const newMenu = WizRoute.segment.menu;
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
