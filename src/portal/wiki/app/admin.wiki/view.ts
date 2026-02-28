import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    public books: any[] = [];
    public keyword: string = '';
    public filterVisibility: string = '';
    public searchFocused: boolean = false;
    public page: number = 1;
    public lastPage: number = 1;
    public total: number = 0;
    public dump: number = 20;

    // 접근 권한 조회
    public selectedBook: any = null;
    public accessList: any[] = [];

    constructor(public service: Service) { }

    public async ngOnInit() {
        await this.loadBooks();
    }

    public async loadBooks() {
        const params: any = {
            page: this.page,
            dump: this.dump,
        };
        if (this.keyword) params.keyword = this.keyword;
        if (this.filterVisibility) params.visibility = this.filterVisibility;

        const { code, data } = await wiz.call("wiki_list", params);
        if (code === 200) {
            this.books = data.rows || [];
            this.total = data.total || 0;
            this.lastPage = data.last_page || 1;
            this.page = data.page || 1;
        }
        await this.service.render();
    }

    public async search() {
        this.page = 1;
        await this.loadBooks();
    }

    public async goPage(p: number) {
        if (p < 1 || p > this.lastPage) return;
        this.page = p;
        await this.loadBooks();
    }

    public pageList(): number[] {
        const pages: number[] = [];
        const maxVisible = 10;
        let start = Math.max(1, this.page - Math.floor(maxVisible / 2));
        let end = Math.min(this.lastPage, start + maxVisible - 1);
        if (end - start + 1 < maxVisible) {
            start = Math.max(1, end - maxVisible + 1);
        }
        for (let i = start; i <= end; i++) {
            pages.push(i);
        }
        return pages;
    }

    public visibilityLabel(vis: string): string {
        const labels: any = { public: '공개', internal: '내부', private: '비공개' };
        return labels[vis] || vis;
    }

    public async viewAccess(book: any) {
        const { code, data } = await wiz.call("wiki_access", { id: book.id });
        if (code === 200) {
            this.selectedBook = data.book;
            this.accessList = data.access || [];
        }
        await this.service.render();
    }

    public closeAccess() {
        this.selectedBook = null;
        this.accessList = [];
    }

    public roleLabel(role: string): string {
        const labels: any = { admin: '관리자', editor: '편집자', viewer: '뷰어' };
        return labels[role] || role;
    }

    public async deleteBook(book: any) {
        const res = await this.service.alert.show({
            title: '위키 삭제',
            status: 'error',
            message: `"${book.title || book.namespace}" 위키를 삭제하시겠습니까?\n모든 페이지와 접근 권한이 함께 삭제됩니다.`,
            action: '삭제',
            actionBtn: 'error',
            cancel: '취소',
        });
        if (!res) return;
        const { code } = await wiz.call("wiki_delete", { id: book.id });
        if (code === 200) {
            this.selectedBook = null;
            this.accessList = [];
            await this.loadBooks();
        }
    }
}
