import { OnInit, Input } from '@angular/core';

export class Component implements OnInit {
    @Input() color = "#0054a6";

    public async ngOnInit() { }
}