import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Project } from '@wiz/libs/portal/works/project';

export class Component implements OnInit {
    constructor(
        public service: Service,
        public project: Project
    ) { }

    public readOnly: boolean = true;
    public newuser: any = { role: 'user' };

    public async ngOnInit() {
        await this.service.init();
        this.readOnly = !this.project.accessLevel(['admin', 'manager']);
        await this.project.member.load();
        await this.service.render();
    }

    public async alert(message: string, status: any = "error", action: string = '확인', cancel: any = false) {
        return await this.service.alert.show({
            title: '',
            message: message,
            cancel: cancel,
            actionBtn: status,
            action: action,
            status: status
        });
    }

    public async roleChanged(user: any) {
        await this.project.member.update(user.user, user.role);
        await this.project.member.load();
        await this.service.render();
    }

    public async remove(user: any) {
        const res = await this.service.alert.show({
            title: "구성원 제외",
            status: "error",
            message: `"${user.meta.name}" 사용자를 이 프로젝트에서 제외하시겠습니까?`,
            action: "제외하기",
            actionBtn: "error",
            cancel: "cancel",
        });
        if (!res) return;
        await this.project.member.remove(user.user);
        await this.project.member.load();
        await this.service.render();
    }

    public async create() {
        let { email, role } = this.newuser;
        email = email.replace(/\s/g, "");
        if (email.length === 0) return;
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailRegex.test(email)) return await this.service.error("Email 포맷이 아닙니다.");
        const { code, data } = await this.project.member.create(email, role);

        if (code != 200) {
            await this.service.error(data);
            return;
        }

        this.newuser = { role: 'user' };
        await this.project.member.load();
        await this.service.render();
    }

}