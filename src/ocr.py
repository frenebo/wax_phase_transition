from  PIL import Image
import sys
import argparse

if __name__ == "__main__":
    source_directory = sys.argv[1]
    selected_regions_strings = sys.argv[2:]
    
    print("Source directory specified: {}".format(source_directory))
    # print("Selected regions specified: {}".format(selected_regions_strings))
    
    region_info = []
    
    for selected_regions_str in selected_regions_strings:
        if len(selected_regions_str.split(":")) != 2:
            raise Exception("Expected colon in format 'identifier:xmin,xmax,ymin,ymax', got '{}'".format(selected_regions_str))
        
        reg_identifier, coords_string = selected_regions_str.split(":")
        
        if len(reg_identifier) == 0 or len(coords_string) == 0:
            raise Exception("Expected format 'identifier:xmin,xmax,ymin,ymax', got '{}'".format(selected_regions_str))
        
        coords_string_split = coords_string.split(",")
        if len(coords_string_split) != 4:
            raise Exception("Expected four integers separated by commas in format 'identifier:xmin,xmax,ymin,ymax', got {}".format(len(coords_string_split)))
        
        xmin,xmax,ymin,ymax = coords_string_split
        
        try:
            xmin=int(xmin)
            xmax=int(xmax)
            ymin=int(ymin)
            ymax=int(ymax)
        except ValueError as e:
            raise Exception("Invalid coordinate in '{}': {}".format(selected_regions_str, e))
        
        if xmax <= xmin:
            raise Exception("Invalid coords in '{}': expected xmax > xmin, but {} <= {}".format(selected_regions_str,xmax,xmin))
        if ymax <= ymin:
            raise Exception("Invalid coords in '{}': expected ymax > ymin, but {} <= {}".format(selected_regions_str,ymax,ymin))
        
        # region_info.
        if reg_identifier in [rid for inf["id"] in region_info]:
            raise Exception("Duplicate identifier '{}'".format(reg_identifier))
        
        region_info.append({
            "id": reg_identifier,
            "xbounds": [xmin,xmax],
            "ybounds": [ymin,ymax],
        })
        
    print("selected regions:")
    for rinfo in region_info:
        print("  {}".format(str(rinfo)))
    
    # for
            
        # selected_regions_str.split9
    # parser = argparse.ArgumentParser("Finds seven segment display numerals from image sequence, in specified zones")
    
    # parser.add_argument("sourcedir")
    
    # args = parser.parse_args()