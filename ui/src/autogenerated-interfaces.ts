export interface CountrySerializer {
    id?: string;
    name: string;
    code: string;
    unicode_flag: string;
}

export interface ServiceSerializer {
    id?: string;
    name: string;
}

export interface RouteSerializer {
    id?: string;
    name: string;
    host_country: CountrySerializer;
}

export interface ProcessStepSerializer {
    id?: string;
    sequence_number: number;
    service: ServiceSerializer;
}

export interface ProcessSerializer {
    id?: string;
    route: RouteSerializer;
    nationality: CountrySerializer;
    home_country?: CountrySerializer;
    steps: ProcessStepSerializer[];
}

export interface ActionSerializer {
    display_name: string;
    name: string;
    url: string;
}

export interface UserSerializer {
    id?: number;
    first_name?: string;
    last_name?: string;
    email?: string;
}

export interface StoredFileSerializer {
    created_by: UserSerializer;
    id?: string;
    media_type: string;
    name: string;
    size: number;
}

export interface ClientSerializer {
    id?: string;
    name: string;
}

export interface ApplicantSerializer {
    id?: string;
    user: UserSerializer;
    employer: ClientSerializer;
    home_country: CountrySerializer;
    nationalities: CountrySerializer[];
}

export interface ClientContactSerializer {
    id?: string;
    user: UserSerializer;
    client: ClientSerializer;
}

export interface ProviderSerializer {
    id?: string;
    logo_url: string;
    name: string;
}

export interface ClientProviderRelationshipSerializer {
    id?: string;
    client: ClientSerializer;
    provider: ProviderSerializer;
    preferred?: boolean;
}

export interface ProviderContactSerializer {
    id?: string;
    user: UserSerializer;
    provider: ProviderSerializer;
}

export interface CaseStepContractSerializer {
    case_step_id?: any;
    provider_contact: ProviderContactSerializer;
    accepted_at?: string;
    rejected_at?: string;
}

export interface CaseStepSerializer {
    id?: string;
    actions: ActionSerializer[];
    active_contract: CaseStepContractSerializer;
    process_step: ProcessStepSerializer;
    sequence_number: number;
    state: any;
    stored_files: StoredFileSerializer[];
}

export interface CaseSerializer {
    id?: string;
    applicant: ApplicantSerializer;
    process: ProcessSerializer;
    steps: CaseStepSerializer[];
    created_at?: string;
    target_entry_date: string;
    target_exit_date: string;
}

