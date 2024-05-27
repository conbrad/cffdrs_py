import numpy as np
import numpy.typing as npt

def buildup_index(dc: npt.NDArray[np.float64], dmc: npt.NDArray[np.float64]):
    """
    Buildup Index Raster Calculation

    Parameters
    ----------
    dc : numpy array of float
       The Drought Code raster
    dmc : numpy array of float
       The Duff Moisture Code raster

    Returns
    -------
    numpy array of float
        Buildup Index

    Notes
    -----
    All code is based on a C code library that was written by Canadian
    Forest Service Employees, which was originally based on
    the Fortran code listed in the reference below. All equations
    in this code refer to that document.

    Equations and FORTRAN program for the Canadian Forest Fire
    Weather Index System. 1985. Van Wagner, C.E.; Pickett, T.L.
    Canadian Forestry Service, Petawawa National Forestry
    Institute, Chalk River, Ontario. Forestry Technical Report 33.
    18 p.

    Additional reference on FWI system

    Development and structure of the Canadian Forest Fire Weather
    Index System. 1987. Van Wagner, C.E. Canadian Forestry Service,
    Headquarters, Ottawa. Forestry Technical Report 35. 35 p.
    """
    # Eq. 27a
    bui1 = np.where((dmc == 0) & (dc == 0), 0, 0.8 * dc * dmc / (dmc + 0.4 * dc))
    
    # Eq. 27b - next 3 lines
    p = np.where(dmc == 0, 0, (dmc - bui1) / dmc)
    cc = 0.92 + ((0.0114 * dmc) ** 1.7)
    bui0 = dmc - cc * p
    
    # Constraints
    bui0 = np.where(bui0 < 0, 0, bui0)
    bui1 = np.where(bui1 < dmc, bui0, bui1)
    
    return bui1