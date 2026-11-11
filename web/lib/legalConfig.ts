/**
 * Centralized Legal and Grievance Configuration for Ready2Code
 * 
 * Note: Under the Digital Personal Data Protection Act (DPDP), 2023 / DPDP Rules, 2025
 * and Information Technology Rules, 2021 (Intermediary Guidelines and Digital Media Ethics Code),
 * verified legal entity, contact, and grievance officer details must be confirmed by the owner
 * and reviewed by qualified Indian counsel prior to commercial operations.
 */

export interface GrievanceOfficerConfig {
  name: string;
  designation: string;
  email: string;
  address: string;
  acknowledgementWindow: string;
  redressalWindow: string;
}

export interface LegalConfig {
  platformName: string;
  legalEntityName: string;
  entityType: string;
  registeredAddress: string;
  supportEmail: string;
  contactEmail: string;
  grievanceOfficer: GrievanceOfficerConfig;
  governingLaw: string;
  jurisdictionVenue: string;
  effectiveDate: string;
  lastUpdated: string;
  termsVersion: string;
  privacyVersion: string;
}

export const LEGAL_CONFIG: LegalConfig = {
  platformName: "Ready2Code",
  legalEntityName: "[OWNER INPUT REQUIRED: Legal Entity Name or Operating Sole Proprietor]",
  entityType: "Educational Technology Platform (Free Launch Tier)",
  registeredAddress: "[OWNER INPUT REQUIRED: Registered Business / Principal Place of Business Address, India]",
  supportEmail: "support@ready2code.dev",
  contactEmail: "contact@ready2code.dev",
  grievanceOfficer: {
    name: "[OWNER INPUT REQUIRED: Grievance Officer Full Name]",
    designation: "Grievance Redressal Officer",
    email: "grievance@ready2code.dev",
    address: "[OWNER INPUT REQUIRED: Grievance Redressal Office Address, India]",
    acknowledgementWindow: "48 hours",
    redressalWindow: "30 days",
  },
  governingLaw: "Republic of India",
  jurisdictionVenue: "[OWNER INPUT REQUIRED: High Court / City Court Jurisdiction, e.g., Bengaluru, Karnataka, India]",
  effectiveDate: "11 November 2026",
  lastUpdated: "11 November 2026",
  termsVersion: "2026-11-11",
  privacyVersion: "2026-11-11",
};
