#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import environment_for_pygimli_build

#boost::python::numeric::array RVector_getArray(GIMLI::RVector & vec)
        #{
            #boost::python::numeric::array::set_module_and_type("numpy", "ndarray");
            #std::cout << "HEREAM_I boost::array" << std::endl;
            #if (!vec.size()) {
            #}
            #boost::python::numeric::array a;
            #return a;
        #}
#"""def( "getArray", &RVector_getArray, 
                #"PyGIMLI Helper Function: extract an array object from an RVector ");""",
            
WRAPPER_DEFINITION_RVector=\
"""
boost::python::tuple RVector_getData(GIMLI::RVector & vec )
        {
            std::cout << "HEREAM_I boost::python::tuple RVector_getData(Gimli::RVector & vec )" << std::endl;
            if (!vec.size()) return boost::python::make_tuple( "none", 0 );
            return boost::python::make_tuple( "none", 0 ); 
        }
"""   
WRAPPER_REGISTRATION_RVector = [   
"""def( "getData", &RVector_getData, 
                "PyGIMLI Helper Function: extract an python object from an RVector ");""",
]                

WRAPPER_DEFINITION_General = \
"""
bool checkDataWrapper() 
{
    std::cout << "checkDataWrapper() called\\n";
    return true;
}

GIMLI::RVector * General_createRVector(boost::python::list listin){
    std::cout << "HEREAM_I GIMLI::RVector * General_createRVector(boost::python::list listin){" << std::endl;
    GIMLI::RVector * ret = new GIMLI::RVector(0);
    return ret;
}
         
"""            
WRAPPER_REGISTRATION_General = [
    """bp::def( "checkDataWrapper", &checkDataWrapper);""",
    """bp::def( "General_createRVector", &General_createRVector, 
                "PyGIMLI Helper Function: create a GIMLI::RVector from given list. Check with custom_rvalue",
                bp::return_value_policy< bp::reference_existing_object, bp::default_call_policies >());""",
     ]

##################################################################

def iter_as_generator_vector(cls):
    print("ITER:", cls.name)
    
    try:
        code = os.linesep.join([ 
                'typedef %(cls)s iter_type;'
                , 'generators::generator_maker_vector< iter_type >::register_< %(call_policies)s >( %(exposer_name)s );'])
        cls.add_registration_code( 
                code % { 'cls' : cls.decl_string
                         , 'call_policies' : cls.mem_fun( 'nextVal' ).call_policies.create_type()
                         , 'exposer_name' : cls.class_var_name }
                , works_on_instance=False )
        cls.include_files.append( 'generators.h' )
        print("OK")
    except:
        raise
        print("FAILED ")
        
#################################################################################################
#################################################################################################

def apply_reg(class_, code):
    for c in code:
        class_.add_registration_code(c)
        
def apply(mb):
    pass
    rt = mb.class_('Vector<double>')
    rt.add_declaration_code(WRAPPER_DEFINITION_RVector)
    apply_reg(rt, WRAPPER_REGISTRATION_RVector)
    #rt.add_registration_code ("""def(bp::init< PyObject * >((bp::arg("value"))))""")
    
    mb.add_declaration_code(WRAPPER_DEFINITION_General)
    apply_reg(mb, WRAPPER_REGISTRATION_General)
        
    #vec_iterators = mb.classes(lambda cls: cls.name.startswith('R'))
        
    vec_iterators = mb.classes(lambda cls: cls.name.startswith('VectorIterator'))
    for cls in vec_iterators:
        iter_as_generator_vector(cls)
