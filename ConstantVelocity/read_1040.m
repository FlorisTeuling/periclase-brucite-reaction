%
% read_1040.m
%
% Function reading an ascii file with a number
% of header lines and a set of columns with values
%
%function [H M] = read_1040(fname, nhlines, separator)
% input: fname    : filename (string)
%        nhlines  : number of header lines (integer)
%        separator: column separator (string)
% output: H : header lines
%         M : matrix with the numerical data

function [H M] = read_1040(fname, nhlines,separator)
  % Get data from the file using the Matlab
  % function importdata
  A = importdata(fname,separator,nhlines);
  % Get the numerical data
  M = A.data;
  % get the headerlines
  H = A.textdata;
end
