from jinja2 import Environment, FileSystemLoader
import os


#This line uses the current directory
file_loader = FileSystemLoader('.')
out_dir = "ROUTE_CONFIGS"


# Load the enviroment
env = Environment(loader=file_loader)
input_file = raw_input("Enter the Route configs:")
local_asn = raw_input("local_asn:")
bgp_neighbor = raw_input("bgp_neighbor:")
remote_asn = raw_input("remote_asn:")
template = env.get_template(input_file)
#Add the varibles


if not os.path.exists(out_dir):
    os.mkdir(out_dir)

output = template.render(local_asn=local_asn, bgp_neighbor=bgp_neighbor, remote_asn=remote_asn)
f = open(os.path.join(out_dir, 'bgp_configs' + ".cfg"), "w")
f.write(output)
f.close()
print("Configuration '%s' created...")
#Print the output
print("Done")