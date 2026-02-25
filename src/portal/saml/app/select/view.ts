import {
    OnInit, Input, Output,
    EventEmitter,
    ElementRef,
    ViewChild,
    HostListener,
    SimpleChanges,
    OnChanges,
} from '@angular/core';
import { Service } from "src/libs/portal/season/service";

// Usage
// wiz-component-select(
//     [options]="nameIDFormats",
//     [multiple]="true",
//     [(value)]="info.NameIDFormat",
//     widthClassName="w-[448px]",
// )

interface SelectOption {
    label: string;
    value: any;
    // icon?: any;
    // iconPosition?: 'left' | 'right';
}

export class Component implements OnInit, OnChanges {
    @Input() options: SelectOption[] = [];
    @Input() value: any | any[];
    @Input() disabled: boolean = false;
    @Input() searchable: boolean = true;
    @Input() placeholder: string = 'Select...';
    @Input() widthClassName: string = 'w-md'; // w-64 등으로 실제 TailwindCSS 클래스 사용
    @Input() className: string = '';
    @Input() multiple: boolean = false;
    @Input() align: 'left' | 'center' | 'right' = 'center';
    @Input() maxHeight: string = '240px';

    @Output() valueChange = new EventEmitter<any | any[]>();

    isOpen: boolean = false;
    focusIndex: number = -1;
    searchText: string = '';

    @ViewChild('container') containerRef!: ElementRef;
    @ViewChild('searchInput') inputRef!: ElementRef<HTMLInputElement>;

    constructor(
        public service: Service,
        private elRef: ElementRef,
    ) { }

    async ngOnInit() {
        await this.service.init();
    }

    get filteredOptions(): SelectOption[] {
        if (!this.searchable) {
            return this.options;
        }
        return this.options.filter((opt) =>
            opt.label.toLowerCase().includes(this.searchText.toLowerCase())
        );
    }

    get selectedOptions(): SelectOption | SelectOption[] | undefined {
        if (this.multiple) {
            return this.options.filter(
                (opt) => Array.isArray(this.value) && this.value.includes(opt.value)
            );
        }
        return this.options.find((opt) => opt.value === this.value);
    }

    get singleSelectedOption(): SelectOption | undefined {
        return this.selectedOptions as SelectOption | undefined;
    }

    get multipleSelectedOptions(): SelectOption[] {
        return (this.selectedOptions as SelectOption[]) || [];
    }

    // useEffect(..., []) -> @HostListener
    @HostListener('document:mousedown', ['$event'])
    handleClickOutside(event: Event) {
        if (!this.elRef.nativeElement.contains(event.target)) {
            this.isOpen = false;
        }
    }

    // onChanges는 @Input 값이 변경될 때마다 호출됩니다.
    ngOnChanges(changes: SimpleChanges): void {
        // 컴포넌트 외부에서 value가 변경되었을 때,
        // 다중 선택 모드에서 선택된 아이템이 없을 경우 드롭다운을 열지 않도록 합니다.
        if (changes['value'] && this.multiple) {
            const prevValue = changes['value'].previousValue;
            const currValue = changes['value'].currentValue;
            if (Array.isArray(prevValue) && Array.isArray(currValue)) {
                if (prevValue.length > 0 && currValue.length === 0) {
                    this.isOpen = false;
                }
            }
        }
    }

    toggleDropdown() {
        if (this.disabled) return;
        this.isOpen = !this.isOpen;

        if (this.isOpen) {
            this.searchText = '';
            this.focusIndex = -1;
            // useEffect([isOpen], ...) -> setTimeout으로 DOM 렌더링 후 포커스
            if (this.searchable) {
                setTimeout(() => this.inputRef.nativeElement.focus(), 0);
            }
        }
    }

    handleKeyDown(e: KeyboardEvent) {
        if (this.disabled) return;

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                if (!this.isOpen) {
                    this.toggleDropdown();
                }
                this.focusIndex =
                    this.focusIndex < this.filteredOptions.length - 1
                        ? this.focusIndex + 1
                        : this.focusIndex;
                break;
            case 'ArrowUp':
                e.preventDefault();
                this.focusIndex = this.focusIndex > 0 ? this.focusIndex - 1 : 0;
                break;
            case 'Enter':
                e.preventDefault();
                if (this.focusIndex >= 0 && this.filteredOptions[this.focusIndex]) {
                    this.handleOptionSelect(this.filteredOptions[this.focusIndex].value);
                }
                break;
            case 'Escape':
                this.isOpen = false;
                this.focusIndex = -1;
                break;
        }
    }

    handleOptionSelect(optionValue: any) {
        if (this.multiple) {
            const currentValue = Array.isArray(this.value) ? [...this.value] : [];
            const index = currentValue.indexOf(optionValue);
            if (index === -1) {
                currentValue.push(optionValue);
            } else {
                currentValue.splice(index, 1);
            }
            this.valueChange.emit(currentValue);
        } else {
            this.valueChange.emit(optionValue);
            this.isOpen = false;
        }
        this.focusIndex = -1;
        if (this.searchable) {
            setTimeout(() => this.inputRef.nativeElement.focus(), 0);
        }
    }

    removeOption(optionValue: any, e: MouseEvent) {
        e.stopPropagation();
        const newValue = (this.value as any[]).filter((v) => v !== optionValue);
        this.valueChange.emit(newValue);
    }
}
