import Project from './project';
import moment from 'moment';
import showdown from 'showdown';

export default class Display {
    constructor(public project: Project) { }

    public todoStatus(todos: any) {
        let checked = 0;
        for (let i = 0; i < todos.length; i++)
            if (todos[i].checked)
                checked++;
        return `${checked}/${todos.length}`;
    }

    public date(date: any) {
        let targetdate = moment(date);
        let diff = new Date().getTime() - new Date(targetdate).getTime();
        diff = diff / 1000 / 60 / 60;
        if (diff > 24) return targetdate.format("YYYY-MM-DD");
        if (diff > 1) return Math.floor(diff) + "시간전"
        diff = diff * 60;
        if (diff < 2) return "방금전";
        return Math.floor(diff) + "분전";
    }

    public markdown(text: string) {
        let converter = new showdown.Converter();
        let html = converter.makeHtml(text);
        // 멘션 하이라이트: @이름을 스타일된 배지로 변환
        // Angular의 [innerHTML] DomSanitizer가 inline style 속성을 제거하므로 class 사용
        html = html.replace(/(^|[\s>])@([^\s<>&]+)/g,
            '$1<span class="wiz-mention">@$2</span>');
        return html;
    }
}