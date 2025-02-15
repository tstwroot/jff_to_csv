import xml.etree.ElementTree as ET
import os

def parse_jflap_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    states = {}
    transitions = []
    initial_state = None
    final_states = set()
    
    # Parse states
    for state in root.findall(".//state"):
        state_id = state.get("id")
        state_name = state.get("name")
        states[state_id] = state_name
        
        if state.find("initial") is not None:
            initial_state = state_name
        if state.find("final") is not None:
            final_states.add(state_name)
    
    # Parse transitions
    for transition in root.findall(".//transition"):
        from_state = states[transition.find("from").text]
        to_state = states[transition.find("to").text]
        read_symbol = transition.find("read").text if transition.find("read").text is not None else "-"
        transitions.append((from_state, read_symbol, to_state))
    
    # Output formatted transitions
    output_lines = []
    for (from_state, read_symbol, to_state) in transitions:
        if from_state == initial_state:
            output_lines.append(f"->{from_state},{read_symbol},{to_state}")
        else:
            output_lines.append(f"{from_state},{read_symbol},{to_state}")
    
    # Output final states
    for final_state in final_states:
        output_lines.append(f"*{final_state},-,-")
    
    return "\n".join(output_lines) + '\n'

def convert_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".jff"):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0].upper().replace(".", "_")
            output_path = os.path.join(output_dir, output_filename)
            
            result = parse_jflap_xml(input_path)
            with open(output_path, "w") as f:
                f.write(result)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert JFLAP XML automata to custom format.")
    parser.add_argument("input_dir", help="Directory containing XML files")
    parser.add_argument("output_dir", help="Directory to save converted files")
    args = parser.parse_args()
    
    convert_directory(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()
