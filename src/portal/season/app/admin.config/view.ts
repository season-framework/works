import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    public activeTab: string = 'site';
    public loading: boolean = false;
    public configData: any = {};

    // 사이트 설정
    public site: any = {
        pwa_title: '',
        pwa_display: 'standalone',
        site_url: '',
    };

    // SMTP 설정
    public smtp: any = {
        smtp_host: '',
        smtp_port: 587,
        smtp_sender: '',
        smtp_password: '',
    };

    // 인증 설정
    public auth: any = {
        auth_saml_use: false,
    };

    // 스토리지 설정
    public storage: any = {
        works_path: '',
        wiki_path: '',
    };

    // SMTP 테스트
    public testEmail: string = '';
    public testLoading: boolean = false;

    // 이메일 템플릿
    public templates: any[] = [];
    public selectedTemplate: any = null;
    public templateContent: string = '';

    public tabs: any[] = [
        { id: 'site', label: '사이트 설정', icon: 'ti ti-world' },
        { id: 'smtp', label: 'SMTP 설정', icon: 'ti ti-mail' },
        { id: 'template', label: '이메일 템플릿', icon: 'ti ti-template' },
        { id: 'auth', label: '인증 설정', icon: 'ti ti-shield-lock' },
        { id: 'storage', label: '스토리지', icon: 'ti ti-database' },
    ];

    constructor(public service: Service) { }

    public async ngOnInit() {
        await this.loadConfig();
    }

    public async loadConfig() {
        this.loading = true;
        await this.service.render();

        const { code, data } = await wiz.call("config_load");
        if (code === 200) {
            this.configData = data;
            this.applyConfig(data);
        }

        this.loading = false;
        await this.service.render();
    }

    private applyConfig(data: any) {
        // 사이트 설정
        if (data.site) {
            for (const item of data.site) {
                if (item.key in this.site) {
                    this.site[item.key] = item.value ?? '';
                }
            }
        }
        // SMTP 설정
        if (data.smtp) {
            for (const item of data.smtp) {
                if (item.key in this.smtp) {
                    this.smtp[item.key] = item.value ?? '';
                }
            }
        }
        // 인증 설정
        if (data.auth) {
            for (const item of data.auth) {
                if (item.key in this.auth) {
                    this.auth[item.key] = item.value;
                }
            }
        }
        // 스토리지 설정
        if (data.storage) {
            for (const item of data.storage) {
                if (item.key in this.storage) {
                    this.storage[item.key] = item.value ?? '';
                }
            }
        }
    }

    public async switchTab(tabId: string) {
        this.activeTab = tabId;
        if (tabId === 'template' && this.templates.length === 0) {
            await this.loadTemplates();
        }
        await this.service.render();
    }

    // ─── 설정 저장 ───

    public async saveSiteConfig() {
        const items = [
            { category: 'site', key: 'pwa_title', value: this.site.pwa_title, type: 'string', description: 'PWA 제목' },
            { category: 'site', key: 'pwa_display', value: this.site.pwa_display, type: 'string', description: 'PWA 디스플레이 모드' },
            { category: 'site', key: 'site_url', value: this.site.site_url, type: 'string', description: '사이트 URL' },
        ];
        await this.saveConfig(items);
    }

    public async saveSmtpConfig() {
        const items = [
            { category: 'smtp', key: 'smtp_host', value: this.smtp.smtp_host, type: 'string', description: 'SMTP 호스트' },
            { category: 'smtp', key: 'smtp_port', value: String(this.smtp.smtp_port), type: 'int', description: 'SMTP 포트' },
            { category: 'smtp', key: 'smtp_sender', value: this.smtp.smtp_sender, type: 'string', description: 'SMTP 발신자' },
            { category: 'smtp', key: 'smtp_password', value: this.smtp.smtp_password, type: 'password', description: 'SMTP 비밀번호' },
        ];
        await this.saveConfig(items);
    }

    public async saveAuthConfig() {
        const items = [
            { category: 'auth', key: 'auth_saml_use', value: String(this.auth.auth_saml_use), type: 'bool', description: 'SAML 인증 사용 여부' },
        ];
        await this.saveConfig(items);
    }

    public async saveStorageConfig() {
        const items = [
            { category: 'storage', key: 'works_path', value: this.storage.works_path, type: 'string', description: 'Works 파일 저장 경로' },
            { category: 'storage', key: 'wiki_path', value: this.storage.wiki_path, type: 'string', description: 'Wiki 파일 저장 경로' },
        ];
        await this.saveConfig(items);
    }

    private async saveConfig(items: any[]) {
        const { code } = await wiz.call("config_update", { data: JSON.stringify(items) });
        if (code === 200) {
            await this.service.alert.show({
                title: '저장 완료',
                status: 'success',
                message: '설정이 저장되었습니다.',
                action: '확인',
            });
            await this.loadConfig();
        } else {
            await this.service.alert.show({
                title: '저장 실패',
                status: 'error',
                message: '설정 저장 중 오류가 발생했습니다.',
                action: '확인',
            });
        }
    }

    // ─── SMTP 테스트 ───

    public async sendTestEmail() {
        if (!this.testEmail) {
            await this.service.alert.show({
                title: '오류',
                status: 'error',
                message: '수신 이메일 주소를 입력해주세요.',
                action: '확인',
            });
            return;
        }
        this.testLoading = true;
        await this.service.render();

        const { code, data } = await wiz.call("smtp_test", { to: this.testEmail });
        this.testLoading = false;
        await this.service.render();

        if (code === 200) {
            await this.service.alert.show({
                title: '발송 완료',
                status: 'success',
                message: data,
                action: '확인',
            });
        } else {
            await this.service.alert.show({
                title: '발송 실패',
                status: 'error',
                message: data || 'SMTP 테스트 실패',
                action: '확인',
            });
        }
    }

    // ─── 이메일 템플릿 ───

    public async loadTemplates() {
        const { code, data } = await wiz.call("template_list");
        if (code === 200) {
            this.templates = data;
        }
        await this.service.render();
    }

    public async selectTemplate(tpl: any) {
        const { code, data } = await wiz.call("template_read", { name: tpl.name });
        if (code === 200) {
            this.selectedTemplate = tpl;
            this.templateContent = data.content;
        }
        await this.service.render();
    }

    public async saveTemplate() {
        if (!this.selectedTemplate) return;
        const { code } = await wiz.call("template_update", {
            name: this.selectedTemplate.name,
            content: this.templateContent,
        });
        if (code === 200) {
            await this.service.alert.show({
                title: '저장 완료',
                status: 'success',
                message: '템플릿이 저장되었습니다.',
                action: '확인',
            });
        }
    }

    public closeTemplate() {
        this.selectedTemplate = null;
        this.templateContent = '';
    }
}
