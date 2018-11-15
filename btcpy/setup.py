# Copyright (C) 2017 chainside srl
#
# This file is part of the btcpy package.
#
# It is subject to the license terms in the LICENSE.md file found in the top-level
# directory of this distribution.
#
# No part of btcpy, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE.md file.
import importlib
from .constants import NETWORKS
from ecdsa.ecdsa import generator_secp256k1, generator_256


MAINNET = None
NETNAME = None
CURVENAME = None


def setup(network='mainnet', force=False):
    global MAINNET, NETNAME, CURVENAME
    if MAINNET is not None and NETNAME != network and not force:
        raise ValueError('Trying to change network type at runtime')
    if network not in NETWORKS:
        raise ValueError('Unknown network type: {}'.format(network))
    MAINNET = (network == 'mainnet')
    NETNAME = network
    CURVENAME = 'NIST256p' if network == 'neo' else 'SECP256k1'


def is_mainnet():
    global MAINNET
    if MAINNET is None:
        raise ValueError('Network type not set')
    return MAINNET


def net_name():
    global NETNAME
    if NETNAME is None:
        raise ValueError('Network type not set')
    if NETNAME == 'regtest':
        return 'testnet'
    return NETNAME


def curve_generator():
    curves = dict(SECP256k1=generator_secp256k1,
                  NIST256p=generator_256)

    return curves[curve_name()]


def privatekey_class():
    """
    For a given curve, return the uninstantiated PrivateKey class
    NIST256p
    SECP256k1
    """
    import_string = 'btcpy.structs.crypto_{}'.format(curve_name())
    return getattr(importlib.import_module(import_string), 'PrivateKey')


def publickey_class():
    """
    For a given curve, return the uninstantiated PublicKey class
    NIST256p
    SECP256k1
    """
    import_string = 'btcpy.structs.crypto_{}'.format(curve_name())
    return getattr(importlib.import_module(import_string), 'PublicKey')


def curve_name():
    global CURVENAME
    if CURVENAME is None:
        raise ValueError('curve name not set')
    return CURVENAME

