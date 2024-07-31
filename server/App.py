#! /usr/bin/python

def warn(*args, **kwargs):
    pass #the trick to switch off deprecation warnings
import warnings
warnings.warn = warn

import numpy as np
import azimuth.model_comparison


def predict(seq, **kwargs):
    """
    Args:
        seq: numpy array of 30 nt sequences.
        kwargs: dictionary of additional optional arguments, including:
            - aa_cut: numpy array of amino acid cut positions (optional).
            - percent_peptide: numpy array of percent peptide (optional).
            - model: model instance to use for prediction (optional).
            - model_file: file name of pickled model to use for prediction (optional).
            - pam_audit: check PAM of each sequence.
            - length_audit: check length of each sequence.
            - learn_options_override: a dictionary indicating which learn_options to override (optional).
    Returns: a numpy array of predictions.
    """
    if type(seq).__module__ != np.__name__:
        seq = np.array(seq)

    aa_cut = kwargs.get('aa_cut')
    if type(aa_cut).__module__ != np.__name__:
        if aa_cut:
            aa_cut = np.array(aa_cut)
        else:
            aa_cut = None

    percent_peptide = kwargs.get('percent_peptide')
    if type(percent_peptide).__module__ != np.__name__:
        if percent_peptide:
            percent_peptide = np.array(percent_peptide)
        else:
            percent_peptide = None

    model = kwargs.get('model', None)
    model_file = kwargs.get('model_file', None)
    pam_audit = kwargs.get('pam_audit', False)
    length_audit = kwargs.get('length_audit', False)
    learn_options_override = kwargs.get('learn_options_override', None)

    predictions = azimuth.model_comparison.predict(
        seq,
        aa_cut=aa_cut,
        percent_peptide=percent_peptide,
        model=model,
        model_file=model_file,
        pam_audit=pam_audit,
        length_audit=length_audit,
        learn_options_override=learn_options_override
    )
    
    result = {seq[i]: prediction for i, prediction in enumerate(predictions)}
    return result


from flask import Flask
from flask import request
from flask.json import jsonify
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
        

@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def info():
    MODEL_FILE_PATH = os.getenv('MODEL_FILE_PATH', 'models/V3_model_full.pickle')
    try:
        if request.method == 'POST':
            json_data = request.get_json(True, False)
            if not json_data or 'sequences' not in json_data:
                logging.error('Sequences not provided in POST request')
                return jsonify({'error': 'Sequences not provided'}), 400
            logging.info(f"Received POST request with data: {json_data}")
            sequences = json_data['sequences']
            seqs = np.array(sequences)
            result = predict(seqs, model_file=MODEL_FILE_PATH)
            #result = predict(seqs)
            return jsonify({'scores': result})
        else:
            sequence = request.args.get('sequence')
            logging.info(f"Received GET request with sequence: {sequence}")
            if sequence: 
                seqs = np.array([sequence])
                result = predict(seqs, model_file=MODEL_FILE_PATH)
                return jsonify({'scores': result})
            else:
                return 'Please, provide a sequence!', 400
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': 'An internal error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5000)