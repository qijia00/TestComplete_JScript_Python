#JIRA ECS_V3-4038: Verify ECU can survive from constant reboot
#------------------------------------------------------------
#function name :  ECS_V3_4038(SSUIP)
#Parameters    :  SSUIP for V3.6
#Description   :  Reboot ECU from Polaris
#------------------------------------------------------------

def ECS_V3_4038(SSUIP):
    
    import time
    
    # Launch Internet Exploer and open Polaris
    URL = "https://{0}/polaris/index.html".format(SSUIP)
    Browsers.Item[btIExplorer].Run(URL)
    browser = Sys.Browser()
    page = browser.Page(URL)
    page.Wait()
    
    # Click "Continue to this website (not recomended)." if the page presents
    overridelink = page.NativeWebObject.Find("id", "overridelink")
    if (overridelink.Exists):
        page.Table(0).Cell(6, 1).Link("overridelink").Click()
        page.Wait()
    
    # Choose Polaris 3D instead of Personal Control if the page presents
    boxbutton3d = page.NativeWebObject.Find("id", "boxbutton3d")
    if (boxbutton3d.Exists):
        page.Panel(0).Panel(1).Panel(0).Panel("boxbutton3d").Link(0).Click()
        page.Wait()
    
    # Login as SysAdmin without password
    page.Form("form1").Panel("silverlightControlHost").Object(0).SlObject("Shell", "").SlObject("CoreRoot").SlObject("BackgroundViewUserControl").SlObject("ContentControl", "").SlObject("Root").SlObject("OKButton").ClickButton()
    page.Wait()    

    # Polaris
    Polaris = page.Form("form1").Panel("silverlightControlHost").Object(0)
    # Polaris Shell
    Polaris_Shell = Polaris.SlObject("Shell", "").SlObject("CoreRoot").SlObject("DefaultLayoutManagerView", "")
    # Top Panel in Polaris Shell
    TopPanel = Polaris_Shell.SlObject("ModeGroupPanel")
    ConfigurePopup = Polaris_Shell.SlObject("ConfigurePopup")

    # Click the [Configure] button on the Top Panel    
    TopPanel.SlObject("RadioButton", "", 0).ClickButton()
    time.sleep(2)
    # Click the [Mapping] button on the Configure Popup
    ConfigurePopup.SlObject("GroupPinnedModes").ClickItem(2)
    page.Wait()
    #time.sleep(20) # First time switch may take up to 30 seconds
    
    # Right Panel in Polaris Shell
    RightPanel = Polaris_Shell.SlObject("EncExpander", "", 1).SlObject("ExpandSite").SlObject("RightToolArea")
    MappingExplorerView = RightPanel.SlObject("EnhancedTabControl", "").SlObject("InternalTabControl").SlObject("MappingExplorerView", "")
    DeviceTree = MappingExplorerView.SlObject("Devices").SlObject("DeviceView", "")
   
    i = 1
    while i <= 6:
        # Click the ECU listed in the Device Tree from the Right Panel
        DeviceTree.SlObject("deviceRadTreeList").SlObject("PART_ItemsScrollViewer").SlObject("PART_GridViewVirtualizingPanel").SlObject("TreeListViewRow", "", 0).Click()
        time.sleep(2)
        # Click the [ShowTools] drop down menu button on the top right coner of the Right Panel
        DeviceTree.SlObject("Button", "").ClickButton()
        time.sleep(2)
        # Polaris DropDown
        Polaris_DropDown = Polaris.SlObject("Popup", "").SlObject("ShowToolsContextMenu")
        # Click [ECU Tools] button from the drop down menu
        Polaris_DropDown.SlObject("RadMenuItem", "", 5).Click()
        time.sleep(2)       
        # Click [Reboot] button from the drop down menu
        Polaris_DropDown.SlObject("RadMenuItem", "", 5).SlObject("PART_Popup").SlObject("ECUReboot").Click()
        time.sleep(2)
        # Polaris Popup
        Polaris_PopUp = Polaris.SlObject("Popup", "").SlObject("DialogView", "").SlObject("ContentControl", "").SlObject("ChoiceView", "")
        # Click Yes to confirme to reboot ECU        
        Polaris_PopUp.SlObject("DialogOKCancelView", "").SlObject("OKButton").ClickButton() 
        time.sleep(60)
        i += 1
    
    # Close the web browser
    browser.Close(5000)
    
#for quick test
def test():
    ECS_V3_4038("10.215.20.121")


