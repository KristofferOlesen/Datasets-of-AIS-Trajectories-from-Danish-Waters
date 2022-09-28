import pandas as pd
import numpy as np
import pickle
import os
import re
import datetime
import math
import torch

from Config import config

def convertShipTypeToName(shipType):
    
    choices = {
        '20': 'Wing in Ground',
        '21': 'Wing in Ground',
        '22': 'Wing in Ground',
        '23': 'Wing in Ground',
        '24': 'Wing in Ground',
        '25': 'Wing in Ground',
        '26': 'Wing in Ground',
        '27': 'Wing in Ground',
        '28': 'Wing in Ground',
        '29': 'SAR Aircraft',
        '30': 'Fishing',
        '31': 'Tug',
        '32': 'Tug',
        '33': 'Dredger',
        '34': 'Dive Vessel',
        '35': 'Military',
        '36': 'Sailing',
        '37': 'Pleasure',
        '40': 'High Speed Vessel',
        '41': 'High Speed Vessel',
        '42': 'High Speed Vessel',
        '43': 'High Speed Vessel',
        '44': 'High Speed Vessel',
        '45': 'High Speed Vessel',
        '46': 'High Speed Vessel',
        '47': 'High Speed Vessel',
        '48': 'High Speed Vessel',
        '49': 'High Speed Vessel',
        '50': 'Pilot',
        '51': 'SAR Ship',
        '52': 'Tug',
        '53': 'Port Tender',
        '54': 'Anti-Pollution',
        '55': 'Law Enforcement',
        '56': 'Local Vessel',  #Local Vessel
        '57': 'Local Vessel',
        '58': 'Medical Transfer',
        '59': 'Special Craft', #eg construction at windmills
        '60': 'Passenger',
        '61': 'Passenger',
        '62': 'Passenger',
        '63': 'Passenger',
        '64': 'Passenger',
        '65': 'Passenger',
        '66': 'Passenger',
        '67': 'Passenger',
        '68': 'Passenger',
        '69': 'Passenger',
        '70': 'Cargo',
        '71': 'Cargo',
        '72': 'Cargo',
        '73': 'Cargo',
        '74': 'Cargo',
        '75': 'Cargo',
        '76': 'Cargo',
        '77': 'Cargo',
        '78': 'Cargo',
        '79': 'Cargo',
        '80': 'Tanker',
        '81': 'Tanker',
        '82': 'Tanker',
        '83': 'Tanker',
        '84': 'Tanker',
        '85': 'Tanker',
        '86': 'Tanker',
        '87': 'Tanker',
        '88': 'Tanker',
        '89': 'Tanker',
        '90': 'Other',
        '91': 'Other',
        '92': 'Other',
        '93': 'Other',
        '94': 'Other',
        '95': 'Other',
        '96': 'Other',
        '97': 'Other',
        '98': 'Other',
        '99': 'Other'
    }
    
    return choices.get(str(shipType), np.nan)

def classNames():
    names = [
        'Cargo',
        'Tanker',
        'Fishing',
        'Passenger',
        'Sailing',
        'Pleasure',
        'High Speed Vessel',
        'Military',
        'Law Enforcement',
        'Pilot',
        'Tug',
        'Dredger',
        'Dive Vessel',
        'Port Tender',
        'Anti-Pollution',
        'Medical Transfer',
        'Local Vessel',
        'Special Craft',
        'SAR Ship',
        'SAR Aircraft',
        'Wing in Ground',
        'Other'
    ]
    
    return np.array(names), len(names)

def readTrajectory(filename, idx):

    with open(filename, 'rb') as file:
        dataSetParams = pickle.load(file)

    index = dataSetParams['indicies'][idx]

    with open(dataSetParams['dataFileName'], 'rb') as file:
        file.seek(index)
        track = pickle.load(file)

    return pd.DataFrame(track)

def readDataset(filename):

    #make dataset
    with open(filename, "rb") as f:
        params = pickle.load(f)

    datapath = params['dataFileName']
    indicies = params['indicies']

    N = len(indicies)

    data = []
    mmsis = []
    shiptypes = []
    lengths = []
    for i, index in enumerate(indicies):
        with open(datapath, 'rb') as file:
            file.seek(index)
            track = pickle.load(file)
            
        tmpdf = pd.DataFrame(track)
        tmpdf['course'] = tmpdf['course'].fillna(value=0)
        
        data_tmp = np.array(tmpdf[['lat','lon','speed','course']].values)
        
        data.append(data_tmp)
        mmsis.append(track['mmsi'])
        shiptypes.append(track['shiptype'])
        lengths.append(track['track_length'])
        
    return data, params, np.array(mmsis), np.array(shiptypes), np.array(lengths)
        
class AISDataset(torch.utils.data.Dataset):
    def __init__(self, infoPath, combined=False, train_preproc = None):
        self.Infopath = infoPath
        self.classnames, self.Nclasses = classNames()
        self.train_preproc = train_preproc

        with open(self.Infopath, "rb") as f:
            self.params = pickle.load(f)
        
        if combined:
            self.indicies = self.params['indicies']
            if self.train_preproc is None:
                self.mean = self.params['mean']
                self.std = self.params['std']
            else:
                self.mean, self.std = self.train_preproc
        elif self.train_preproc is None:
            self.indicies = self.params['trainIndicies']
            self.mean = self.params['train_mean']
            self.std = self.params['train_std']
        else:
            self.indicies = self.params['testIndicies']
            self.mean, self.std = self.train_preproc
        
        self.datapath = self.params['dataFileName']        
        self.datasetN = len(self.indicies)
                     
        self.labels, self.lengths, self.mmsis = self.getLabels()
        
        if 'outlierLabels' in self.params.keys():
            self.outliers = self.params['outlierLabels']
                    
    def __len__(self):
        return self.datasetN

    def __getitem__(self, idx):
            
        index = self.indicies[idx]
        
        with open(self.datapath, 'rb') as file:
            file.seek(index)
            track = pickle.load(file)
        
        typeName = convertShipTypeToName(str(track['shiptype']))
        label = np.where(typeName==self.classnames)[0][0] if typeName is not np.nan else -1
        length = track['track_length']        
        
        tmpdf = pd.DataFrame(track)
        tmpdf['course'] = tmpdf['course'].fillna(value=0)    
        targets = torch.tensor(tmpdf[['lat','lon','speed','course']].values, dtype=torch.float)
        inputs = (targets - self.mean)/self.std
    
        return  torch.tensor(track['mmsi']), np.array(track['timestamp']), torch.tensor(label), torch.tensor(length, dtype=torch.long), inputs, targets
            
    def getLabels(self):
        
        labels = []
        lengths = []
        mmsis = []
        with torch.no_grad():
            for index in self.indicies:
                with open(self.datapath,'rb') as file:
                    file.seek(index)
                    track = pickle.load(file)
                    typeName = convertShipTypeToName(str(track['shiptype']))
                    
                    if typeName is not np.nan:
                        labels.append(np.where(typeName==self.classnames)[0][0])
                    else:
                        labels.append(-1)
                    
                    mmsis.append(track['mmsi'])
                    lengths.append(track['track_length'])
                            
        return torch.tensor(labels), torch.tensor(lengths), torch.tensor(mmsis)
        
    def getDataObservation(self, idx):
            
        index = self.indicies[idx]
        
        with open(self.datapath, 'rb') as file:
            file.seek(index)
            track = pickle.load(file)
            
        return pd.DataFrame(track)

    def reconstruct(self, encodedTrack):
        recon = encodedTrack * self.std + self.mean
            
        return recon

