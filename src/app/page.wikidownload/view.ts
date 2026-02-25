import { OnInit } from '@angular/core';
import { ElementRef, ViewChild } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { WikiBook } from '@wiz/libs/portal/wiki/book';

export class Component implements OnInit {

    @ViewChild('printarea')
    public printElement: ElementRef;

    @ViewChild('editor')
    public editorElement: ElementRef;
    public editor: any;

    public DOC_ID: string = "";

    constructor(public service: Service, public wikibook: WikiBook) {
        if (!WizRoute.segment.id)
            return service.href("/");
        this.DOC_ID = WizRoute.segment.id;
    }

    public async ngOnInit() {
        await this.service.init();
        await this.service.auth.allow();
        const { code, data } = await wiz.call("load", { id: this.DOC_ID });
        let editor = await this.wikibook.bindEditor(this.editorElement.nativeElement, false);
        if (editor) this.editor = editor;
        this.editor.data.set(data);

        document.getElementsByTagName("html")[0].style.overflow = 'auto';
        document.body.style.height = 'auto';
        document.getElementsByTagName('app-root')[0].style.height = 'auto';
    }
}