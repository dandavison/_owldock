/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export type ProviderContactList = ProviderContact[];
export type StoredFileList = StoredFile[];

export interface BaseModel {}
export interface Provider {
  uuid: string;
  name: string;
  logo_url: string;
}
export interface ProviderContact {
  uuid: string;
  user: User;
  provider: Provider;
}
export interface User {
  uuid: string;
  first_name: string;
  last_name: string;
  email: string;
}
export interface StoredFile {
  uuid: string;
  created_by: User;
  media_type: string;
  name: string;
  size: number;
}
