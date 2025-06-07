import { Institution } from "./Institution";
import { Subject } from "./Subject";

export class Course {
    constructor(public id: number, public name: string, public institution: Institution, public aps: number, public subjects: Subject[]){}

}