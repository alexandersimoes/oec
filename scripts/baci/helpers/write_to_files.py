import os, bz2

def write_to_files(year, dfs, output_path, hs_revision):
    for df in dfs:
        name, data = df
        
        '''reorder columns so year is first'''
        data = data.reset_index()
        data["year"] = year
        cols = data.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        data = data[cols]
        
        '''create new BZ2 formatted file'''
        new_file_path = os.path.abspath(os.path.join(output_path, "hs{}_{}.tsv.bz2".format(hs_revision, name)))
        print ' writing file: ', name
        data.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep="\t", index=False, na_rep="\N")