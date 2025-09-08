import { OnInit } from "@angular/core";
import { Service } from "src/libs/portal/season/service";

export class Component implements OnInit {
    public O = Object;
    constructor(
        public service: Service,
    ) { }

    async ngOnInit() {
        await this.service.init();
        await this.load();
    }

    public nameIDFormats = [
        "urn:oasis:names:tc:SAML:2.0:nameid-format:persistent",
        "urn:oasis:names:tc:SAML:2.0:nameid-format:transient",
        "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified",
        "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
    ].map(it => ({ label: it, value: it }));
    public samlAttributes = [];

    public info = null;
    public async load() {
        const { code, data } = await wiz.call("load");
        if (code != 200) return await this.service.error("Error!");
        const { config, saml_attributes } = data;
        if (Object.keys(config.org).length === 0) config.org = { name: "", display_name: "", url: "" };
        if (Object.keys(config.contact).length === 0) config.contact = { name: "", email: "", type: "technical" };
        if (!config.NameIDFormat) config.NameIDFormat = [];
        if (!config.required_attributes) config.required_attributes = [];
        if (!config.optional_attributes) config.optional_attributes = [];
        this.info = config;
        this.samlAttributes = saml_attributes.map(({ name, uri }) => ({
            label: `${name} (${uri})`,
            value: uri,
        }));
        await this.service.render();
    }

    public async update() {
        const body = this.service.copy(this.info);
        body.public_key = this.info.public_key.path;
        body.private_key = this.info.private_key.path;

        await this.service.loading.show();
        const { code } = await wiz.call("update", body);
        await this.service.loading.hide();
        if (code !== 200) return await this.service.error("Error!");
        await this.service.success("Saved");
        await this.load();
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
