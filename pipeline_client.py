import win32file
import win32pipe, win32file

PIPE_NAME = r'\\.\pipe\MyPipe'

def start_client():
    # Connect to the named pipe server
    pipe = win32file.CreateFile(
                PIPE_NAME,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0, None, win32file.OPEN_EXISTING, 0, None)

    print("Connected to server.")
    # Send the initial message to the server
    message = input("Enter message: ")
    win32file.WriteFile(pipe, message.encode('utf-8'))
    while True:
        result, data = win32file.ReadFile(pipe, 64*1024)
        response:str=data.decode('utf-8')
        print(f"Received from server: {response}")
        if "ExportFiles" in response:
            is_exported="files are exported successfully,FILE_EXPORT_COMPLETED"
            win32file.WriteFile(pipe, is_exported.encode('utf-8'))                
        elif "GetSavingDirectory" in response:
            saving_path="saving directory is determined successfully"
            win32file.WriteFile(pipe, saving_path.encode('utf-8'))                
        elif "UserInquiryMessage" in response:
            response_message = input("Enter message: ")
            win32file.WriteFile(pipe, response_message.encode('utf-8'))   
        elif "GetRevitModelsDirectories" in response:
            Revit_paths="Revit directories are determined successfully"
            win32file.WriteFile(pipe, Revit_paths.encode('utf-8'))
        elif "InsertPrices" in response:
            prices_insertion="prices are inserted succesfully successfully,PRICE_INSERTION_COMPLETED"
            win32file.WriteFile(pipe, prices_insertion.encode('utf-8'))
        elif "LoadingSharedParamterFile" in response:
            shared_parameter_loading="Shared Parameter is Loaded successfully"
            win32file.WriteFile(pipe, shared_parameter_loading.encode('utf-8'))
        elif "GetCategoriesForCurrentDocument" in response:
            win32file.WriteFile(pipe, categories.encode('utf-8'))    
        elif "GetSimilarCategories" in response:
            walls_similar_categories="OST_MassWallsAll, OST_Walls, OST_StackedWalls"
            win32file.WriteFile(pipe, walls_similar_categories.encode('utf-8'))          
        elif "GenerateCategorySchedule" in response:
            Revit_paths="category schedule is generated successfully,SCHEDULE_COMPLETED"
            win32file.WriteFile(pipe, Revit_paths.encode('utf-8')) 
        elif "ChatEnd" in response:
            Revit_paths="Revit directories are determined successfully"
            win32file.WriteFile(pipe, Revit_paths.encode('utf-8'))                         
        if response.lower() == "closed":
            break
        # Flush the pipe to clear any existing data
        #win32file.FlushFileBuffers(pipe) 

    # Close the named pipe
    win32file.CloseHandle(pipe)

categories = """OST_RevisionClouds, OST_DetailComponents, OST_IOS_GeoSite, OST_CurtainWallPanels, 
OST_Roofs, OST_StructuralFoundation, OST_BuildingPad, OST_RoofSoffit, OST_Ceilings, 
OST_Grids, OST_Stairs, OST_Ramps, OST_Cornices, OST_GenericModel, OST_StructuralFramingSystem, 
OST_CurtaSystem, OST_Fascia, OST_Gutter, OST_EdgeSlab, OST_MassWallsAll, OST_MassRoof, OST_MassFloorsAll, 
OST_MassShade, OST_MassGlazingAll, OST_MassOpening, OST_SiteProperty, OST_CoverType, OST_PipeMaterials, 
OST_PipeConnections, OST_PipeSchedules, OST_WireMaterials, OST_WireInsulations, OST_WireTemperatureRatings, 
OST_ConduitStandards, OST_Wire, OST_ElectricalVoltage, OST_ElecDistributionSys, OST_Fluids, OST_DuctSystem, 
OST_PipingSystem, OST_StairsCutMarks, OST_StairsPaths, OST_StairsRuns, OST_StairsLandings, OST_StairsStringerCarriage, 
OST_LinksAnalytical, OST_DuctCurves, OST_FlexDuctCurves, OST_PipeCurves, OST_FlexPipeCurves, OST_CableTray, OST_Conduit, 
OST_ViewportLabel, OST_Levels, OST_ProfileFamilies, OST_ColorFillLegends, OST_Walls, OST_RailingHandRail, OST_Floors, 
OST_TitleBlocks, OST_GenericAnnotation, OST_RasterImages, OST_IOSDetailGroups, OST_Doors, OST_CalloutHeads, OST_LevelHeads, 
OST_SectionHeads, OST_ElevationMarks, OST_StructConnectionSymbols, OST_StructuralBracePlanReps, OST_SpotElevSymbols, 
OST_DetailComponentTags, OST_ReferenceViewerSymbol, OST_MultiCategoryTags, OST_KeynoteTags, OST_WindowTags, OST_DoorTags, 
OST_WallTags, OST_RoomTags, OST_MaterialTags, OST_NurseCallDevices, OST_AnalyticalPipeConnections, OST_CurtainWallMullions, 
OST_SpecialityEquipment, OST_PlumbingFixtures, OST_GridHeads, OST_CeilingTags, OST_MechanicalEquipmentSet, OST_MEPSystemZone, 
OST_TilePatterns, OST_Casework, OST_Reveals, OST_StairsRailing, OST_LightingFixtures, OST_Furniture, OST_RvtLinks, 
OST_StairsTrisers, OST_IOSModelGroups, OST_MechanicalEquipment, OST_StackedWalls, OST_Windows, OST_RailingTopRail, 
OST_StairsRailingBaluster, OST_RailingTermination, OST_CommunicationDevices, 
OST_SecurityDevices, OST_Site, OST_StructConnections, OST_StructuralFraming, OST_StructuralColumns, 
OST_StructuralColumnTags, OST_Toposolid, OST_RebarBendingDetails"""
if __name__ == '__main__':
    start_client()