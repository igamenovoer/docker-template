# main command of PeiDocker utility
import logging

# configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s]\t%(message)s')

import click
import os
import shutil

import omegaconf as oc
from pei_docker.config_processor import *
        
@click.group()
def cli():
    pass

# TODO: generate build.sh and run.sh scripts
    
# create the output dir and copy the template files there
@click.command()
@click.option('--project-dir', '-p', help='project directory', required=True, 
              type=click.Path(exists=False, file_okay=False))
def create(project_dir):
    logging.info(f'Creating PeiDocker project in {project_dir}')
    os.makedirs(project_dir, exist_ok=True)
    
    # the directory should be empty
    if len(os.listdir(project_dir)) > 0:
        logging.error(f'Directory {project_dir} is not empty')
        return
    
    # copy all the files and folders in project_files to the output dir
    this_dir : str = os.path.dirname(os.path.realpath(__file__))
    project_template_dir = f'{this_dir}/project_files'    
    for item in os.listdir(project_template_dir):
        s = os.path.join(project_template_dir, item)
        d = os.path.join(project_dir, item)
        if os.path.isdir(s):
            logging.info(f'Copying directory {s} to {d}')
            shutil.copytree(s, d)
        else:
            logging.info(f'Copying file {s} to {d}')
            shutil.copy2(s, d)
            
    # copy config and compose template files to the output dir
    src_config_template : str = f'{this_dir}/{Defaults.ConfigTemplatePath}'
    dst_config_template : str = f'{project_dir}/{Defaults.OutputConfigName}'
    logging.info(f'Copying config template {src_config_template} to {dst_config_template}')
    shutil.copy2(src_config_template, dst_config_template)
    
    src_compose_template : str = f'{this_dir}/{Defaults.ComposeTemplatePath}'
    dst_compose_template : str = f'{project_dir}/{Defaults.OutputComposeTemplateName}'
    logging.info(f'Copying compose template {src_compose_template} to {dst_compose_template}')
    shutil.copy2(src_compose_template, dst_compose_template)
    
    logging.info('Done')
        
# generate the docker compose file from the config file
@click.command()
@click.option('--project-dir', '-p', help='project directory', required=True, 
              type=click.Path(exists=False, file_okay=False))
@click.option('--config', '-c', default=f'{Defaults.OutputConfigName}', help='config file name, relative to the project dir', 
              type=click.Path(exists=False, file_okay=True, dir_okay=False))
@click.option('--full-compose', '-f', is_flag=True, default=False, help='generate full compose file with x-??? sections')
def configure(project_dir:str, config:str, full_compose:bool):
    logging.info(f'Configuring PeiDocker project from {project_dir}/{config}')
    
    # read the config file
    config_path : str = os.path.join(project_dir, config)
    in_config = oc.OmegaConf.load(config_path)
    
    # read the compose template file
    compose_path : str = os.path.join(project_dir, Defaults.OutputComposeTemplateName)
    in_compose = oc.OmegaConf.load(compose_path)
    
    # process the config file
    proc : PeiConfigProcessor = PeiConfigProcessor.from_config(in_config, in_compose, project_dir=project_dir)
    out_compose = proc.process(remove_extra=not full_compose)
    out_yaml = oc.OmegaConf.to_yaml(out_compose)
    
    # write the compose file to the same directory as config file
    out_compose_path = os.path.join(project_dir, Defaults.OutputComposeName)
    logging.info(f'Writing compose file to {out_compose_path}')
    with open(out_compose_path, 'w') as f:
        f.write(out_yaml)
    
    logging.info('Done')
        
cli.add_command(create)
cli.add_command(configure)

if __name__ == '__main__':
    # Run the command line interface
    cli()