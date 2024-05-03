//declare module 'flexsearch/dist/module/document' {
//  type Document = {
//    id: string | number;
//    content: string;
//  };
//
//  export default Document;
//}

declare module "flexsearch/dist/module/document" {
  export interface IndexDefinition {
    field: string;
    tokenize: string;
  }

  export interface DocumentOptions {
    id: string;
    index: IndexDefinition[];
  }

  interface DocumentObject {
    time: string;
    content: string;
  }

  type FlexSearchResult = string[];

  export default class Document {
    constructor(options: DocumentOptions);
    add(document: DocumentObject): Index;
    search(query: string): FlexSearchResult;
  }
}
