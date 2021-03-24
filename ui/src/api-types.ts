export interface UserSerializer {
    id?: number;
    password: string;
    last_login?: string;
    is_superuser?: boolean;
    username: string;
    first_name?: string;
    last_name?: string;
    email?: string;
    is_staff?: boolean;
    is_active?: boolean;
    date_joined?: string;
    groups?: any[];
    user_permissions?: any[];
}

export interface EmployeeSerializer {
    id?: number;
    created_at?: string;
    modified_at?: string;
    home_country: string;
    user?: any;
    employer?: any;
}

export interface CaseSerializer {
    id?: number;
    created_at?: string;
    modified_at?: string;
    service: string;
    host_country: string;
    target_entry_date: string;
    status: string;
    progress: number;
    client_contact?: any;
    provider_contact?: any;
    employee?: any;
    process?: any;
}

