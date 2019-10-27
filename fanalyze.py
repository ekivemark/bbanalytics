#!/usr/bin/env python
# fanalyze.py
# Collect EOB Summary

import os
import sys
import json

FPATH = "./data/explanationofbenefit"

SUMMARY_FILE = "./data/eob_summary.json"
RESULT_FILE = "./data/eob_result.csv"

def get_ids():

    # prepare the
    w = open(SUMMARY_FILE, "w+")
    csv = open(RESULT_FILE,"a+")
    # write the opening of a list
    w.write("[")

    eob_list = []
    fl = get_file_list()

    fl_c = len(fl)
    print("Files to process: %s" % fl_c)
    n = 0
    skip_file = 0
    for i in fl:
        n += 1
        fn = build_pathspec(i)
        jd = get_json(fn)

        bundle_id = get_bundle_id(jd)
        t = get_total_eobs(jd)

        if t > 0:
            analysis = get_eob_id(jd)
            # print(".", end="")
            sys.stdout.write(".")
            sys.stdout.flush()

            if bundle_id:
                summary = {"file": fn,
                           "bundleId": bundle_id,
                           "total": t,
                           "analysis": analysis}
                eob_list.append(summary)
                pretty_summary = json.dumps(summary,
                                            indent=4,
                                            sort_keys=True)
                w.write(pretty_summary)
                w.write(",\n")
                # print(i, t)

                if summary is None:
                    pass
                else:
                    print_summary = str(n) + ", -" + summary['file'][len(FPATH) + 1:-5]
                    if 'analysis' in summary:
                        if len(summary['analysis']) > 0:
                            if 'types' in summary['analysis']:
                                print_summary = "%s, %s, %s" % (print_summary,
                                                                t,
                                                                summary['analysis']['types'])

                    csv.write(print_summary + "\n")

                    # print(print_summary)
            summary = {}
        else:
          skip_file += 1
    w.write("\n]")

    print("\nFiles processed:%s" % fl_c)
    print("\nFiles skipped:%s" % skip_file)

    w.close()
    csv.close()
    return eob_list


def get_file_list():

    fl = []
    for file in os.listdir(FPATH):
        if file.endswith(".json"):
            fl.append(file)

    fl.sort()

    return fl


def build_pathspec(n):

    fn = FPATH + "/" + n
    return fn


def get_json(fn):
    # Get json file

    f = open(fn, "r")

    jd = json.load(f)

    return jd


def get_bundle_id(jd):
    # get eob id
    if 'id' in jd:
        return jd['id']
    else:
        return


def get_total_eobs(jd):
    if 'total' in jd:
        return jd['total']
    else:
        return 0


def get_patient(entry):
    # get patient id

    p = (entry['resource']['patient']['reference'])

    p.split("/")

    return "%s/-%s" % (p[0], p[1])

def get_eob_id(jd):
    # get individual eob info

    if 'entry' not in jd:
        # jt = json.dumps(jd, indent=4, sort_keys=True)
        # print(jt[0:300])
        return {}
    entries = jd['entry']

    patient = []
    eob_list = []
    eob_type = {}
    summary_diag_list = []
    for e in entries:
        diag_list = []
        eob_id = e['resource']['id']
        eob_list.append(eob_id)
        e_type = eob_id.split("-")
        if e_type[0] in eob_type:
            ct = eob_type[e_type[0]]
            eob_type[e_type[0]] = ct + 1
        else:
            eob_type[e_type[0]] = 1
        p = get_patient(e)
        if p not in patient:
            patient.append(p)
        dl = get_diagnosis(e['resource'])

        diag_list = summarize_diagnosis(diag_list, dl)
        summary_diag_list = summarize_diagnosis(summary_diag_list,
                                                diag_list)
        if diag_list is None:
            pass
        else:
            # print(diag_list)
            pass
    mt = len(eob_type)
    eob_analysis = {'eob_list': eob_list,
                    'patient': patient,
                    'types': eob_type,
                    'multiType': mt,
                    'diagnosis': summary_diag_list}
    return eob_analysis


def get_diagnosis(entry):
    # get diagnosis[x]
    #              ['diagnosisCodeableConcept']
    #              ['coding']

    # print(entry)
    diag_list = []
    if 'diagnosis' in entry:

        # print('got diagnosis')
        for dl in entry['diagnosis']:
            # print(dl)
            if 'diagnosisCodeableConcept' in dl:
                if 'coding' in dl['diagnosisCodeableConcept']:
                    # print('got coding')
                    for c in dl['diagnosisCodeableConcept']['coding']:
                        # print(c)
                        if c not in diag_list:
                            diag_list.append(c)

    return diag_list


def summarize_diagnosis(dlist, dl):
    # get the items in the dl and see if they are already in dlist

    new_dlist = dlist

    for d in dl:
        if d not in dlist:
            new_dlist.append(d)
    if new_dlist is None:
        return []

    return new_dlist

