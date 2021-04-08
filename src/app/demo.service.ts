import {Injectable} from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

const httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable()
export class DemoService {

    constructor(private http:HttpClient) {
    }

    // Uses http.get() to load data from a single API endpoint
    getFoods() {
        return this.http.get('https://localhost:3000/api/food', {responseType: 'text'});
    }

    // Uses http.get() to load data from a single API endpoint
    process(text) {
        return this.http.get('https://localhost:3000/api/process'+encodeURIComponent(text));
    }

}
