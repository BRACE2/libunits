classdef UnitHandler < dynamicprops
  methods
    function obj = UnitHandler(units)
	[data_path,~,~] = fileparts(mfilename('fullpath'));
        fid = fopen(fullfile(data_path,'defs.json'));
	raw = fread(fid,inf);
	defs = jsondecode(char(raw'));
	fclose(fid);
	obj = defs
    end
  end
end
