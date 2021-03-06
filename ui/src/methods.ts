import { Applicant as IApplicant } from "./autogenerated-interfaces/client";

export function applicantUnicodeFlags(applicant: IApplicant): string {
  return applicant.nationalities
    .map((nationality) => nationality.unicode_flag)
    .join(" ");
}
