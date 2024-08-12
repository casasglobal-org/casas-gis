@echo off
for /L %%G in (1,1,10) do (
if %%G EQU 3 (
echo %%G
) else (
echo %%G is not 3
)
)
