export interface CountrySerializer {
    id?: number;
    name: string;
    code: string;
    unicode_flag: string;
}

export interface ServiceSerializer {
    id?: number;
    name: string;
}

export interface RouteSerializer {
    id?: number;
    name: string;
    host_country: CountrySerializer;
}

export interface ProcessStepSerializer {
    id?: number;
    sequence_number: number;
    service: ServiceSerializer;
}

export interface ProcessSerializer {
    id?: number;
    route: RouteSerializer;
    nationality: CountrySerializer;
    home_country?: CountrySerializer;
    steps: ProcessStepSerializer[];
}

export interface UserSerializer {
    id?: number;
    first_name?: string;
    last_name?: string;
    email?: string;
}

export interface ClientSerializer {
    id?: number;
    name: string;
}

export interface ApplicantSerializer {
    id?: number;
    user: UserSerializer;
    employer: ClientSerializer;
    home_country: CountrySerializer;
    nationalities: CountrySerializer[];
}

export interface ClientContactSerializer {
    id?: number;
    user: UserSerializer;
    client: ClientSerializer;
}

export interface ProviderSerializer {
    id?: number;
    name: string;
}

export interface ProviderContactSerializer {
    id?: number;
    user: UserSerializer;
    provider: ProviderSerializer;
}

export interface CaseStepSerializer {
    id?: number;
    process_step: ProcessStepSerializer;
    sequence_number: number;
    stored_files: any[];
}

export interface CaseSerializer {
    id?: number;
    applicant: ApplicantSerializer;
    provider_contact: ProviderContactSerializer;
    process: ProcessSerializer;
    steps: CaseStepSerializer[];
    created_at?: string;
    target_entry_date: string;
    target_exit_date: string;
}

