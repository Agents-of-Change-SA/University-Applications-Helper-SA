export class User {
    constructor(public id: number, public email: string, public first_name: string, public last_name: string) {}

    getFullName(): string {
        return this.last_name;
    }
}