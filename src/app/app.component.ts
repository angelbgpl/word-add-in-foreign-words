import { Component } from '@angular/core';
import {DemoService} from './demo.service';
import {Observable} from 'rxjs/Rx';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  public foods;

  public text;
  
  public bodyText;

  public results;
  
  constructor(private _demoService: DemoService) { 
   }

  async process() {
    var documentText = '1232';

    return Word.run(async context => {
    var documentBody = context.document.body;
    context.load(documentBody);
    await context.sync();
    documentText = documentBody.text;

    await this.processRequest(documentText);
    // console.log(this.results);
    
    // console.log(this.results);

    // documentBody.insertParagraph(this.results,
    //                     "Start");
    // await context.sync();
    });
  }

  async show() {
    return Word.run(async context => {
      console.log(this.results);
      var docBody = context.document.body;
          docBody.insertParagraph(this.results,
          "Start");
    await context.sync();
    });
  }

  processRequest(text) {
    this._demoService.process(text).subscribe(
      data => {
        //console.log(data);
        this.results = data;
        // console.log(data.replace('&', '\n'));
        Word.run(async context => {
          var docBody = context.document.body;
              // docBody.insertParagraph(data,
              // "Start");
        await context.sync();
        });
        // refresh the list
      }
   );
   console.log(this.results);
  }
  
  title = 'OfficeAddin';
}
