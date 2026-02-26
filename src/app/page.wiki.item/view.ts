import { OnInit, OnDestroy } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { Subscription } from 'rxjs';
import { Service } from '@wiz/libs/portal/season/service';
import { Project } from '@wiz/libs/portal/works/project';
import { WikiBook } from '@wiz/libs/portal/wiki/book';

export class Component implements OnInit, OnDestroy {
    public BOOK_ID: string = "";
    public CONTENT_ID: string = "";

    public loaded: boolean = false;
    private routerSub: Subscription;

    constructor(
        public service: Service,
        public wikibook: WikiBook,
        public project: Project,
        private router: Router
    ) {
        if (!WizRoute.segment.id)
            return service.href("/explore/wiki");
        this.BOOK_ID = WizRoute.segment.id;
        if (!WizRoute.segment.content)
            return service.href(`/wiki/${this.BOOK_ID}/home`);
    }

    public async ngOnInit() {
        if (this.project.prev) {
            await this.project.init(this.project.prev);
        }
        await this.service.init();
        await this.service.auth.allow();
        await this.wikibook.init(this.BOOK_ID);
        if (!this.wikibook.status())
            return this.service.href("/explore/wiki");
        
        this.CONTENT_ID = WizRoute.segment.content;
        this.loaded = true;

        this.routerSub = this.router.events.subscribe(async (event) => {
            if (event instanceof NavigationEnd) {
                if (!this.loaded) return;
                const newContentId = WizRoute.segment.content;
                if (newContentId && newContentId !== this.CONTENT_ID) {
                    this.CONTENT_ID = newContentId;
                    await this.wikibook.content.load(this.CONTENT_ID);
                    await this.service.render();
                }
            }
        });

        await this.service.render();
    }

    public async ngOnDestroy() {
        if (this.routerSub) this.routerSub.unsubscribe();
        await this.service.render();
    }
}
