-- Language
insert into language (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Unknown','U',1,sysdate(),1,sysdate(),1);
insert into language (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Sanskrit','sa',1,sysdate(),1,sysdate(),1);
insert into language (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Hindi','hn',1,sysdate(),1,sysdate(),1);
insert into language (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Tamil','ta',1,sysdate(),1,sysdate(),1);
insert into language (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Kannada','kn',1,sysdate(),1,sysdate(),1);
insert into language (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Telugu','te',1,sysdate(),1,sysdate(),1);
insert into language (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Malayalam','ma',1,sysdate(),1,sysdate(),1);
insert into language (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('English','eng',1,sysdate(),1,sysdate(),1);

-- Script
insert into script (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Unknown','U',1,sysdate(),1,sysdate(),1);
insert into script (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Devanagari','dn',1,sysdate(),1,sysdate(),1);
insert into script (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Tamil','ta',1,sysdate(),1,sysdate(),1);
insert into script (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Kannada','kn',1,sysdate(),1,sysdate(),1);
insert into script (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Telugu','te',1,sysdate(),1,sysdate(),1);
insert into script (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Malayalam','ma',1,sysdate(),1,sysdate(),1);
insert into script (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Grantha','gn',1,sysdate(),1,sysdate(),1);
insert into script (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Maithili','mt',1,sysdate(),1,sysdate(),1);
insert into script (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Kanarese','ka',1,sysdate(),1,sysdate(),1);
insert into script (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Latin','la',1,sysdate(),1,sysdate(),1);
insert into script (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Nandinagari','na',1,sysdate(),1,sysdate(),1);
insert into script (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Roman','rom',1,sysdate(),1,sysdate(),1);
insert into script (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Malayalam and Grantha','mag',1,sysdate(),1,sysdate(),1);

-- Category
insert into category (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Original text','ot',1,sysdate(),1,sysdate(),1);
insert into category (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Compilation','co',1,sysdate(),1,sysdate(),1);
insert into category (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Commentary','cm',1,sysdate(),1,sysdate(),1);
insert into category (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Original text with Commentary','otwc',1,sysdate(),1,sysdate(),1);
insert into category (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Sub Commentary','sc',1,sysdate(),1,sysdate(),1);

-- Type
insert into type (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Unknown','U',1,sysdate(),1,sysdate(),1);
insert into type (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Poetry','po',1,sysdate(),1,sysdate(),1);
insert into type (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Prose','pr',1,sysdate(),1,sysdate(),1);
insert into type (name, short_name, created_by,created_at,updated_by,updated_at,active)
values('Prose and Poetry','pp',1,sysdate(),1,sysdate(),1);

-- branch
insert into branch (name, short_name, indic_name, created_by,created_at,updated_by,updated_at,active)
values('Science & Technology','ST','',1,sysdate(),1,sysdate(),1);

-- discipline
insert into discipline (name, short_name, indic_name, branch_id, created_by,created_at,updated_by,updated_at,active)
values('Physical Sciences','PS','भौतिकविज्ञानम्',1,1,sysdate(),1,sysdate(),1);
insert into discipline (name, short_name, indic_name, branch_id, created_by,created_at,updated_by,updated_at,active)
values('Mathematics','MT','गणितशास्त्रम्',1,1,sysdate(),1,sysdate(),1);
insert into discipline (name, short_name, indic_name, branch_id, created_by,created_at,updated_by,updated_at,active)
values('Health and Life Sciences','HLS','आरोग्य-जीवविज्ञानम्',1,1,sysdate(),1,sysdate(),1);
insert into discipline (name, short_name, indic_name, branch_id, created_by,created_at,updated_by,updated_at,active)
values('Earth and Environmental Sciences','EES','पृथ्वी एवं पर्यावरणविज्ञानम्',1,1,sysdate(),1,sysdate(),1);
insert into discipline (name, short_name, indic_name, branch_id, created_by,created_at,updated_by,updated_at,active)
values('Applied Sciences','AS','आन्वयिक विज्ञानम्',1,1,sysdate(),1,sysdate(),1);
insert into discipline (name, short_name, indic_name, branch_id, created_by,created_at,updated_by,updated_at,active)
values('Social Sciences','SS','समाजविज्ञानम्',1,1,sysdate(),1,sysdate(),1);

-- Subject
-- Physical Sciences
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Astronomy','AS','खगोलशास्त्रम्',1,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Physics','PH','भौतिकशास्त्रम्',1,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Chemistry','CH','रसायनशास्त्रम्',1,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Biology','BIO','जीवशास्त्रम्',1,1,sysdate(),1,sysdate(),1);

-- Mathematics
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Applied Mathematics','AM','आन्वयिक गणितशास्त्रम्',2,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Measurement','MS','मापनम्',2,1,sysdate(),1,sysdate(),1);

-- Health and Life Sciences
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Nursing','NU','परिचर्याशास्त्रम्',3,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Neuro Science','NS','स्नायुविज्ञानम्',3,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Pharmacology','PC','औषधविज्ञानम्',3,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Toxicology','TO','विषविज्ञानम्',3,1,sysdate(),1,sysdate(),1);

-- Earth and Environmental Sciences
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Ecology','EC','पर्यावरणशास्त्रम्',4,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Geography','GE','भूगोलविज्ञानम्',4,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Botany','BO','वनस्पतिविज्ञानम्',4,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Atmospheric Sciences','ATS','वायुमण्डलविज्ञानम्',4,1,sysdate(),1,sysdate(),1);

-- Applied Sciences
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Food Science','FS','आहारविज्ञानम्',5,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Engineering','ENG','अभियांत्रिकीविज्ञानम्',5,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Architecture','ARC','वास्तुशास्त्रम्',5,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Crystallography','CR','स्फटिकविज्ञानम्',5,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Gemmology','GEM','रत्नविज्ञानम्',5,1,sysdate(),1,sysdate(),1);

-- Social Sciences
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Military Science','MTS','सैन्यविज्ञानम्',6,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Political Science','POL','राजनीतिविज्ञानम्',6,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Linguistics','LS','भाषाविज्ञानम्',6,1,sysdate(),1,sysdate(),1);
insert into subject (name, short_name, indic_name, discipline_id, created_by,created_at,updated_by,updated_at,active)
values('Behavioural Sciences','BS','मानसविज्ञानम्',6,1,sysdate(),1,sysdate(),1);