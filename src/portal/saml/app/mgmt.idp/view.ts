import { OnInit } from "@angular/core";
import { Service } from "src/libs/portal/season/service";
import { validateIdpMetadata } from "src/libs/portal/saml/metadata";

export class Component implements OnInit {

    constructor(
        public service: Service,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.load();
    }

    public list = [];
    public newItem = null;
    public async load() {
        const { code, data } = await wiz.call("load");
        if (code !== 200) return await this.service.error("Failed to load IdP Providers");
        this.list = data;
        await this.service.render();
    }

    public modal = null;
    public async viewXML(item) {
        const { code, data } = await wiz.call("xml", { id: item.id });
        if (code !== 200) return await this.service.error("Failed to load XML");
        this.modal = { display_name: item.display_name, xml: data };
        await this.service.render();
    }

    public async updateIcon(item) {
        let res = await this.service.alert.show({
            title: '',
            message: '아이콘을 변경하시겠습니까?',
            cancel: '닫기',
            actionBtn: 'warning',
            action: '확인',
            status: 'warning'
        });
        if (!res) return;

        let icon = await this.service.file.read({ type: 'image', accept: 'image/*', width: 96, quality: 1 });
        item.icon = icon;
        await this.service.render();
    }

    public deleteIcon(item) {
        item.icon = null;
        this.service.render();
    }

    public add() {
        this.newItem = {
            key: "",
            use: true,
            display_name: "",
            xml_content: "",
        };
        this.service.render();
    }

    public async update(item) {
        const body = this.service.copy(item);
        if (body.key.replace(/\s/g, "").length === 0) return await this.service.error(`"key" is a required field.`);
        if (body.display_name.replace(/\s/g, "").length < 4) return await this.service.error(`Please enter at least 4 characters for "Display Name".`);
        if (!item.id) {
            if (body.xml_content.replace(/\s/g, "").length === 0) return await this.service.error(`"Metadata" is a required field.`);
            const validate = await this.validateMetadata(body.xml_content);
            if (!validate) return;
        }
        const { code, data } = await wiz.call("update", body);
        if (code !== 200) return await this.service.error(data);
        await this.service.success("Success to update");
        this.newItem = null;
        await this.load();
    }

    public async remove(item) {
        let res = await this.service.alert.show({
            title: '',
            message: 'IdP를 삭제하시겠습니까?',
            cancel: '닫기',
            actionBtn: 'error',
            action: '삭제하기',
            status: 'error'
        });
        if (!res) return;
        const body = { key: item.key };
        const { code } = await wiz.call("remove", body);
        if (code !== 200) return await this.service.error("Failed to remove IdP");
        await this.service.success("Success to remove");
        await this.load();
    }

    public async validateMetadata(xmlString) {
        try {
            const errors = validateIdpMetadata(xmlString);
            if (errors.length > 0) {
                await this.service.error(errors.map(it => `- ${it}`).join("\n"));
                return false;
            }
        } catch (err) {
            console.error(err);
            await this.service.error("Invalid Metadata");
            return false;
        }
        return true;
    }

    public showCopied = false;
    public async copyToClipboard(text) {
        await navigator.clipboard.writeText(text);
        this.showCopied = true;
        await this.service.render();
        setTimeout(() => {
            this.showCopied = false;
            this.service.render();
        }, 1000);
    };
}