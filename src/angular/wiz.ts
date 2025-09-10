import { io } from "socket.io-client";

export default class Wiz {
    public namespace: any;
    public baseuri: any;

    constructor(baseuri: any) {
        this.baseuri = baseuri;
    }

    public app(namespace: any) {
        let instance = new Wiz(this.baseuri);
        instance.namespace = namespace;
        return instance;
    }

    public dev() {
        let findcookie = (name) => {
            let ca: Array<string> = document.cookie.split(';');
            let caLen: number = ca.length;
            let cookieName = `${name}=`;
            let c: string;

            for (let i: number = 0; i < caLen; i += 1) {
                c = ca[i].replace(/^\s+/g, '');
                if (c.indexOf(cookieName) == 0) {
                    return c.substring(cookieName.length, c.length);
                }
            }
            return '';
        }

        let isdev = findcookie("season-wiz-devmode");
        if (isdev == 'true') return true;
        return false;
    }

    public project() {
        let findcookie = (name) => {
            let ca: Array<string> = document.cookie.split(';');
            let caLen: number = ca.length;
            let cookieName = `${name}=`;
            let c: string;

            for (let i: number = 0; i < caLen; i += 1) {
                c = ca[i].replace(/^\s+/g, '');
                if (c.indexOf(cookieName) == 0) {
                    return c.substring(cookieName.length, c.length);
                }
            }
            return '';
        }

        let project = findcookie("season-wiz-project");
        if (project) return project;
        return "main";
    }

    public socket() {
        let socketns = this.baseuri + "/app/" + this.project();
        if (this.namespace)
            socketns = socketns + "/" + this.namespace;
        return io(socketns);
    }

    public url(function_name: string) {
        if (function_name[0] == "/") function_name = function_name.substring(1);
        return this.baseuri + "/api/" + this.namespace + "/" + function_name;
    }

    public async call(api: string, body = {}, options = {}) {
        let res;
        const uri = this.url(api);

        try {
            if (body) {
                res = await fetch(uri, {
                    method: "post",
                    body: JSON.stringify(body),
                    headers: { 'Content-Type': 'application/json' },
                    ...options,
                });
            }
            else {
                res = await fetch(uri);
            }
            try {
                res = await res.clone().json();
            } catch (err) {
                if (res.status !== 200)
                    return { code: res.status, data: res.statusText };
                else {
                    const data = await res.text();
                    return { code: res.status, data };
                }
            }
        } catch (err) {
            return { code: 500, data: err };
        }
        return res;
    }
}