import { OnInit } from "@angular/core";
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    public currentSection: string = 'user';
    public currentSubsection: string = '';

    public menus: any[] = [
        { id: 'user', label: '사용자 관리', icon: 'ti ti-users' },
        { id: 'project', label: '프로젝트 관리', icon: 'ti ti-folder' },
        { id: 'wiki', label: '위키 관리', icon: 'ti ti-book-2' },
        { id: 'saml', label: 'SAML 설정', icon: 'ti ti-shield-lock' },
        { id: 'config', label: '시스템 설정', icon: 'ti ti-settings' },
    ];

    constructor(
        public service: Service,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.service.auth.allow.membership("admin", "/explore/project");

        const section = WizRoute.segment?.section;
        if (section) {
            this.currentSection = section;
        } else {
            this.service.href('/admin/user');
            return;
        }

        const subsection = WizRoute.segment?.subsection;
        if (subsection) {
            this.currentSubsection = subsection;
        }

        await this.service.render();
    }

    public isActive(menuId: string): boolean {
        return this.currentSection === menuId;
    }

    public navigate(menuId: string) {
        this.currentSection = menuId;
        this.currentSubsection = '';
        this.service.href(`/admin/${menuId}`);
    }
}
